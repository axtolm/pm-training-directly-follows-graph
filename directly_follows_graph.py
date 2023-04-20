# -*- coding: utf-8 -*-
"""
Created on April 16, 2023
@author: Alexander Tolmachev axtolm@gmail.com
A streamlit web app "Process Mining training" - Module "Directly-Follows Graph (DFG)"

"""
# packages
import streamlit as st
import pandas as pd
import graphviz
import itertools
import re

# default settings of the page
st.set_page_config(page_title="PM-training (DFG)", page_icon=":rocket:", 
                   layout= "wide", initial_sidebar_state="expanded")
# hide right menu and logo at the bottom 
hide_streamlit_style = """
                       <style>
                       #MainMenu {visibility: unhidden;}
                       footer {visibility: hidden;}
                       </style>
                       """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)              

def main():
    # =============================================================================
    LNG = 'en'                  # interface language
    md_text = get_dict_text()   # dict with markdown texts
    # =============================================================================
    # left panel      
    # =============================================================================
    page = st.sidebar.radio('**Directly Follows Graph (DFG)**', 
                            ['Baseline Discovery Algorithm','DFG matrix & footprint',
                             'Activity-Based Filtering','Variant-Based Filtering','Arc-Based Filtering'
                             ]) 
    dfg_orientation = st.sidebar.radio('**DFG orientation (Left → Right or Top → Bottom)**',['LR','TB'],index = 0, horizontal = True)
    st.sidebar.markdown('---')
    st.sidebar.markdown(md_text['left_block_author_refs',LNG])                    
    # =============================================================================   
    # central panel
    # =============================================================================   
    st.markdown('##### Process Mining training. Directly-Follows Graph (DFG)')   
    # =============================================================================
    # common block #0 - Context and Definitions
    with st.expander("DFG Contents and Definitions", expanded = False):
        # Show Definition (Directly-Follows Graph)
        st.markdown(md_text['cb_recall_dfg_def',LNG]) 
        st.info(md_text['cb_dfg_definition',LNG])
        st.markdown(md_text['cb_contents',LNG]) 
    
    # =============================================================================
    # common block #1 - event log selection 
    st.markdown(md_text['common_block',LNG])    
    with st.expander("Select an event log for training", expanded = True):
        # show the default simple event logs
        st.markdown(md_text['log_list',LNG])
        # selection radio buttons
        st_radio_select_log = st.radio('Choose one of the default event logs or create your own', 
                                     ('L1','L2','L3','L4','L5','L6','L7','L8','Create event log'), 
                                       index = 0, horizontal = True)
        # form selected_log as string
        if st_radio_select_log == 'Create event log':
            selected_log = st.text_input('Input your event log as a string', value = '[<acd>45, <bce>42]')
            st.markdown(md_text['user_log_format_requirements',LNG])
        else: selected_log = get_default_event_log(st_radio_select_log)
    # =============================================================================    
    # common block #2 - check the selected event log 
    with st.expander("Check the selected event log in the table format", expanded = True): 
        try:
            df_log = get_df_log(selected_log)
            if len(df_log)==0: raise Exception ('Error! Check your input data')   # simple error test
            st.write(df_log)   # show DataFrame
        except Exception as ex_msg: st.warning(ex_msg)        
    
    # =========================================================================
    # Exercise #1 - DFG (Baseline Discovery Algorithm)
    # =========================================================================
    if page == 'Baseline Discovery Algorithm':  
        st.markdown('##### Constructing a Directly-Follows Graph (DFG): Baseline Discovery Algorithm')  
        with st.form('Get DFG elements - nodes and arcs with their quantities'):
            st_submitt_get_dfg = st.form_submit_button('Get DFG elements - nodes and arcs with their quantities')
            if st_submitt_get_dfg:
                # =========================================================================
                # executive python code
                # =========================================================================
                df_log['trace'] = 'I' + df_log['trace'] + 'O'  # add start & end
                DFG_nodes, DFG_arcs = get_DFG (list(df_log['trace']), list(df_log['qty'])) # get DFG nodes & arcs
                vDFG = get_vDFG(DFG_arcs, DFG_nodes, dfg_orientation,'I','O')   # construct DFG as graphviz object
                # =========================================================================
                # web-page             
                # Show Definition (Baseline Discovery Algorithm for DFG)
                st.markdown(md_text['p1_recall_disc_dfg_def',LNG])
                with st.expander("Definition (Baseline Discovery Algorithm for DFG) [1]", expanded = True):
                    st.info(md_text['p1_discovery_dfg_definition',LNG])
                
                # STEP 1. Add Start (I) and End (O) to all traces
                st.markdown(md_text['p1_step_1_add_I_O',LNG])
                st.write(df_log) # visualization df_log as an intermediate result
                with st.expander("Step 1 (example)", expanded = True):
                    st.info(md_text['p1_step_1_algorithm',LNG])    # example for step 1

                st.markdown(md_text['p1_step_2_3_intro',LNG])                
                
                # STEP 2. Calculate a set of activities A with their  frequencies for DFG = (A,F) 
                st.markdown(md_text['p1_step_2_title',LNG])                
                st.write(DFG_nodes)    # visualization DFG_nodes as an intermediate result
                with st.expander("Step 2 (example)", expanded = True): # example for step 2
                    st.info(md_text['p1_step_2_algorithm',LNG])                     
              
                # STEP 3. Calculate a set of arcs F with their frequencies for DFG = (A,F)
                st.markdown(md_text['p1_step_3_title',LNG])
                st.write(DFG_arcs)    # visualization DFG_arcs as an intermediate result
                with st.expander("Step 3 (example)", expanded = True):
                    st.info(md_text['p1_step_3_algorithm',LNG])     # example for step 2
                
                # STEP 4. Show the DFG
                st.markdown(md_text['p1_step_4_title',LNG])
                st.image(vDFG) # show DFG
                st.markdown(md_text['p1_step_4_summary',LNG])
                st.success(md_text['p1_step_1_2_3_4_summary',LNG], icon="✅")
                
    # =========================================================================
    # Exercise #2 - DFG matrix & footprint
    # =========================================================================                        
    elif (page == 'DFG matrix & footprint'): 
        st.markdown('##### Constructing a DFG matrix and DFG footprint')  
        with st.form('Get DFG matrix representation & DFG footprint'):
            st_submitt_get_dfg_footprint = st.form_submit_button('Get DFG matrix representation & DFG footprint')
            if st_submitt_get_dfg_footprint:
                # =========================================================================
                # executive python code
                # =========================================================================
                df_log['trace'] = 'I' + df_log['trace'] + 'O'  # add start & end
                DFG_nodes, DFG_arcs = get_DFG (list(df_log['trace']), list(df_log['qty'])) # get DFG nodes & arcs
                # construct DFG matrix and footprint
                df_footprint, dict_footprint, df_dfg_matrix, dict_dfg_matrix = get_footprint_matrix(list(DFG_arcs['pair']),list(DFG_arcs['qty']),'I','O')
                # =========================================================================
                # web-page forming                
                # DFG matrix
                st.markdown(md_text['p2_step_1_title',LNG]) 
                st.markdown(md_text['p2_dfg_matrix_intro',LNG])
                st.write(df_dfg_matrix)
                with st.expander("Step 1 (example)", expanded = True):
                    st.info(md_text['p2_step_1_algorithm',LNG])    # example for step 1                    
                st.markdown(md_text['p2_dfg_matrix_comment',LNG])
                # DFG footprint
                st.markdown(md_text['p2_step_2_title',LNG]) 
                st.markdown(md_text['p2_dfg_footprint_intro',LNG])
                with st.expander("Definition (Footprint) [1]", expanded = True):
                    st.info(md_text['p2_dfg_footprint_definition',LNG])
                st.write(df_footprint)
                with st.expander("Step 2 (example)", expanded = True):
                    st.info(md_text['p2_step_2_algorithm',LNG])    # example for step 2     

                st.success(md_text['p2_step_1_2_summary',LNG], icon="✅")

    # =========================================================================
    # Exercise #3 - Activity-Based Filtering
    # =========================================================================                 
    elif (page == 'Activity-Based Filtering'): 
        st.markdown('##### Activity-Based Filtering')
        st.markdown(md_text['p3_abf_definition_intro',LNG])
        with st.expander("Definition (Activity-Based Filtering) [1]", expanded = True):
             st.info(md_text['p3_abf_definition',LNG])
        # =========================================================================
        # executive python code
        # DFG based on the original event log
        df_log['trace'] = 'I' + df_log['trace'] + 'O'  # add start & end to each trace (original)
        DFG_nodes, DFG_arcs = get_DFG (list(df_log['trace']), list(df_log['qty'])) # get DFG nodes & arcs (original)
        vDFG = get_vDFG(DFG_arcs, DFG_nodes, dfg_orientation,'I','O')   # construct DFG as graphviz object (original)
        # =========================================================================
        max_activity_slider = int(DFG_nodes['qty'].sort_values().max())    # max frequency value for the slider
        # =========================================================================
        # Slider for tau(act), full set of activities and filtered activities in 3 columns      
        col1,col2,col3 = st.columns([1,1,2])      
        # column 1
        activity_frequency = col1.slider('Select a threshold τ(act) [1]', 
                                       min_value= 0, max_value = max_activity_slider, 
                                       value = int(max_activity_slider*3/4), step = 1, format='%f')
        col1.markdown(md_text['p3_slider_comment',LNG] % (activity_frequency))
        # column 2
        col2.markdown(md_text['p3_full_a_tab',LNG])
        col2.write(DFG_nodes[~DFG_nodes['act'].isin(['I','O'])])
        # column 3
        col3.markdown(md_text['p3_filtered_a_tab',LNG] % (activity_frequency))
        # =========================================================================
        # executive python code
        # get dataframe with filtered activities
        abf_A = DFG_nodes[(DFG_nodes['qty'] >= activity_frequency)&(~DFG_nodes['act'].isin(['I','O']))].copy()
        # =========================================================================
        col3.write(abf_A)
        col3.markdown(md_text['p3_note_start_end',LNG])
        # =========================================================================
        
        with st.form('Apply the Activity-Based Filtering'):
            st_submitt_activity_based_filtering = st.form_submit_button('Apply the Activity-Based Filtering')
            if st_submitt_activity_based_filtering:
                # step 1 - Get the projection of L on a subset of filtered activities A
                # =========================================================================
                # executive python code
                # get the projecion of trace on a subset of activities               
                def get_trace_projection(trace, act):
                    res = []
                    for s in trace: 
                        if (s in act): res.append(s)
                    return ''.join(res)                
                df_log['trace_projection'] = list(map(lambda trace: get_trace_projection(trace, list(abf_A['act'])), df_log['trace']))
                df_log['trace_projection'] = 'I' + df_log['trace_projection'] + 'O'  # add start & end
                # =========================================================================   
                st.markdown(md_text['p3_step_1_title',LNG])
                st.write(df_log)                
                with st.expander("Step 1 (example)", expanded = True):
                    st.info(md_text['p3_step_1_example',LNG])
                # step 1 - Get the projection of L on a subset of filtered activities A
                # =========================================================================
                # executive python code
                abf_DFG_nodes, abf_DFG_arcs = get_DFG (list(df_log['trace_projection']), list(df_log['qty'])) # get DFG nodes & arcs after filtering
                abf_vDFG = get_vDFG(abf_DFG_arcs, abf_DFG_nodes, dfg_orientation,'I','O')   # construct DFG as graphviz object
                # =========================================================================
                st.markdown(md_text['p3_step_2_title',LNG])
                st.markdown(md_text['p3_step_2_subtitle',LNG])
                # original & filtered DFGs in 4 columns                
                col1,col2,col3,col4 = st.columns([1,1,1,1])    
                # col 1
                col1.markdown(md_text['p3_step_2_col1_original_nodes',LNG])
                col1.dataframe(DFG_nodes)
                #col 2
                col2.markdown(md_text['p3_step_2_col2_original_arcs',LNG])
                col2.dataframe(DFG_arcs)
                #col 3
                col3.markdown(md_text['p3_step_2_col3_filtered_nodes',LNG])
                col3.write(abf_DFG_nodes)     
                # col 4
                col4.markdown(md_text['p3_step_2_col4_filtered_arcs',LNG])
                col4.write(abf_DFG_arcs)
                # original & filtered visual DFGs in 2 columns  
                col1,col2 = st.columns([1,1])
                # col 1
                col1.markdown(md_text['p3_step_2_co1_original_dfg',LNG])                
                col1.image(vDFG) # show DFG
                # col 2
                col2.markdown(md_text['p3_step_2_co2_filtered_dfg',LNG]) 
                col2.image(abf_vDFG)
                
                st.success(md_text['p3_step_1_2_summary',LNG], icon="✅")
                
    # =========================================================================
    # Exercise #4 - Variant-Based Filtering
    # =========================================================================  
    elif (page == 'Variant-Based Filtering'): 
        st.markdown('##### Variant-Based Filtering')
        st.markdown(md_text['p4_vbf_definition_intro',LNG])
        with st.expander("Definition (Variant-Based Filtering) [1]", expanded = True):
             st.info(md_text['p4_vbf_definition',LNG])
        # =========================================================================
        # executive python code
        # DFG based on the original event log
        df_log['trace'] = 'I' + df_log['trace'] + 'O'  # add start & end to each trace (original)
        DFG_nodes, DFG_arcs = get_DFG (list(df_log['trace']), list(df_log['qty'])) # get DFG nodes & arcs (original)
        vDFG = get_vDFG(DFG_arcs, DFG_nodes, dfg_orientation,'I','O')   # construct DFG as graphviz object (original)
        # =========================================================================
        max_variant_slider = int(df_log['qty'].sort_values().max())    # max frequency value for the slider  
        # =========================================================================
        # Slider for tau(var), full log and filtered log in 3 columns      
        col1,col2,col3 = st.columns([1,1,2])      
        # column 1
        variant_frequency = col1.slider('Select a threshold τ(var) [1]', 
                                       min_value= 0, max_value = max_variant_slider, 
                                       value = int(max_variant_slider*3/4), step = 1, format='%f')
        col1.markdown(md_text['p4_slider_comment',LNG] % (variant_frequency))
        # column 2
        col2.markdown(md_text['p4_full_v_tab',LNG])
        col2.write(df_log.sort_values(by=['qty'], ascending=False))
        # column 3
        col3.markdown(md_text['p4_filtered_v_tab',LNG] % (variant_frequency))
        # =========================================================================
        # executive python code
        # get dataframe with filtered activities
        vbf_L = df_log[df_log['qty'] >= variant_frequency].sort_values(by=['qty'], ascending=False).copy()
        vbf_DFG_nodes, vbf_DFG_arcs = get_DFG (list(vbf_L['trace']), list(vbf_L['qty'])) # get DFG nodes & arcs after filtering
        vbf_vDFG = get_vDFG(vbf_DFG_arcs, vbf_DFG_nodes, dfg_orientation,'I','O')   # construct DFG as graphviz object        
        # =========================================================================
        col3.write(vbf_L)
        # =========================================================================
        
        with st.form('Apply the Variant-Based Filtering'):
            st_submitt_variant_based_filtering = st.form_submit_button('Apply the Variant-Based Filtering')
            if st_submitt_variant_based_filtering:
                st.markdown(md_text['p4_step_1_title',LNG])
                st.markdown(md_text['p4_step_1_subtitle',LNG])
                # original & filtered DFGs in 4 columns                
                col1,col2,col3,col4 = st.columns([1,1,1,1])    
                # col 1
                col1.markdown(md_text['p4_step_1_col1_original_nodes',LNG])
                col1.dataframe(DFG_nodes)
                #col 2
                col2.markdown(md_text['p4_step_1_col2_original_arcs',LNG])
                col2.dataframe(DFG_arcs)
                #col 3
                col3.markdown(md_text['p4_step_1_col3_filtered_nodes',LNG])
                col3.write(vbf_DFG_nodes)     
                # col 4
                col4.markdown(md_text['p4_step_1_col4_filtered_arcs',LNG])
                col4.write(vbf_DFG_arcs)
                # original & filtered visual DFGs in 2 columns  
                col1,col2 = st.columns([1,1])
                # col 1
                col1.markdown(md_text['p4_step_1_co1_original_dfg',LNG])                
                col1.image(vDFG) # show DFG
                # col 2
                col2.markdown(md_text['p4_step_1_co2_filtered_dfg',LNG]) 
                col2.image(vbf_vDFG)
                
                st.success(md_text['p4_step_1_summary',LNG], icon="✅")
                
    # =========================================================================
    # Exercise #5 - Arc-Based Filtering
    # =========================================================================               
    elif (page == 'Arc-Based Filtering'): 
        st.markdown('##### Arc-Based Filtering')
        st.markdown(md_text['p5_arc_bf_definition_intro',LNG])
        with st.expander("Definition (Arc-Based Filtering) [1]", expanded = True):
             st.info(md_text['p5_arc_bf_definition',LNG])
        
        # =========================================================================
        # executive python code
        # DFG based on the original event log
        df_log['trace'] = 'I' + df_log['trace'] + 'O'  # add start & end to each trace (original)
        DFG_nodes, DFG_arcs = get_DFG (list(df_log['trace']), list(df_log['qty'])) # get DFG nodes & arcs (original)
        vDFG = get_vDFG(DFG_arcs, DFG_nodes, dfg_orientation,'I','O')   # construct DFG as graphviz object (original)
        # =========================================================================
        max_arc_slider = int(DFG_arcs['qty'].sort_values().max())    # max frequency value for the slider
        # =========================================================================
        # Slider for tau(arc), full arcs and filtered arcs in 3 columns      
        col1,col2,col3 = st.columns([1,1,2])      
        # column 1
        arc_frequency = col1.slider('Select a threshold τ(arc) [1]', 
                                       min_value= 0, max_value = max_arc_slider, 
                                       value = int(max_arc_slider*3/4), step = 1, format='%f')
        col1.markdown(md_text['p5_slider_comment',LNG] % (arc_frequency))
        # column 2
        col2.markdown(md_text['p5_full_arc_tab',LNG])
        col2.write(DFG_arcs)
        # column 3
        col3.markdown(md_text['p5_filtered_arc_tab',LNG] % (arc_frequency))
        # =========================================================================
        # executive python code
        # get dataframe with filtered activities
        arc_bf_DFG_arcs = DFG_arcs[DFG_arcs['qty'] >= arc_frequency].copy()
        arc_bf_DFG_nodes = DFG_nodes.copy()
        arc_bf_vDFG = get_vDFG(arc_bf_DFG_arcs, arc_bf_DFG_nodes, dfg_orientation,'I','O')   # construct DFG as graphviz object        
        # =========================================================================
        col3.write(arc_bf_DFG_arcs)
        # =========================================================================
        
        with st.form('Apply the Arc-Based Filtering'):
            st_submitt_variant_based_filtering = st.form_submit_button('Apply the Arc-Based Filtering')
            if st_submitt_variant_based_filtering:
                st.markdown(md_text['p5_step_1_title',LNG])
                st.markdown(md_text['p5_step_1_subtitle',LNG])
                # original & filtered DFGs in 4 columns                
                col1,col2,col3,col4 = st.columns([1,1,1,1])    
                # col 1
                col1.markdown(md_text['p5_step_1_col1_original_nodes',LNG])
                col1.dataframe(DFG_nodes)
                #col 2
                col2.markdown(md_text['p5_step_1_col2_original_arcs',LNG])
                col2.dataframe(DFG_arcs)
                #col 3
                col3.markdown(md_text['p5_step_1_col3_filtered_nodes',LNG])
                col3.write(arc_bf_DFG_nodes)     
                # col 4
                col4.markdown(md_text['p5_step_1_col4_filtered_arcs',LNG])
                col4.write(arc_bf_DFG_arcs)
                # original & filtered visual DFGs in 2 columns  
                col1,col2 = st.columns([1,1])
                # col 1
                col1.markdown(md_text['p5_step_1_co1_original_dfg',LNG])                
                col1.image(vDFG) # show DFG
                # col 2
                col2.markdown(md_text['p5_step_1_co2_filtered_dfg',LNG]) 
                col2.image(arc_bf_vDFG)
                
                st.markdown(md_text['p5_step_1_pre_summary',LNG]) 
                st.success(md_text['p5_step_1_summary',LNG], icon="✅")
        
# =============================================================================
# Service functions
# =============================================================================
# Common block 
# =============================================================================
def get_df_log(str_log):
    '''
    Event log transformation from str ('[<acd>45, <bce>42]') to pandas.DataFrame (columns = ['trace','qty'])
    '''
    return pd.DataFrame({'trace':re.findall('[a-z]+', str_log),'qty':[int(s) for s in re.findall('[0-9]+', str_log)]})
# =============================================================================
# Exercise #1 - DFG (Baseline Discovery Algorithm)
# =============================================================================
def get_DFG (traces_list, qty_list):
    '''
    Computing the DFG nodes - (activity, frequency), and
    the DFG arcs - ((activity,activity), frequency)

    Parameters
    ----------
    traces_list : list
        list of traces (e.g. traces_list = ['acd','bce'])
    qty_list : list
        list of frequencies of traces (e.g. qty_list = [45,42] )
    Returns
    -------
    DFG_nodes_agg : pandas.DataFrame
        2 columns: 'act' - activities, 'qty' - their frequencies in the event log
    DFG_arcs_agg : pandas.DataFrame
        2 columns: 'pair' - arcs, 'qty' - their frequencies in the event log
    
    Example
    -------
    DFG_nodes, DFG_arcs = get_DFG (list(df_log['trace']), list(df_log['qty']))
    '''   
    # create internal pd.DataFrame based on input data
    L = pd.DataFrame({'trace_full':traces_list, 'qty': qty_list})
    # =============================================================================
    # NODES (ACTIVITIES)
    # function get_activities returns pd with pairs (activity, frequency) for one trace ('abc') with frequency (20)
    get_activities = lambda trace, qty: pd.DataFrame({'act':list(trace),'qty':qty})
    # compute DFG nodes as pd for all traces using the function get_activities
    L['nodes'] = list(map(lambda trace, qty: get_activities(trace, qty), L['trace_full'], L['qty']))
    # merge and aggregate all DFG nodes with sorting in descending frequency
    DFG_nodes = pd.concat([L.iloc[i]['nodes'] for i in list(L.index)])
    DFG_nodes_agg = pd.DataFrame(DFG_nodes.groupby(['act']).sum()).sort_values(by=['qty'], ascending=False).reset_index()
    # =============================================================================
    # EDGES (ARCS)
    # function get_pairs returns pd with pairs (arc, frequency) for one trace ('abc') with frequency (20)
    get_pairs = lambda trace, qty: pd.DataFrame({'pair':list(map(lambda s1, s2: s1 + s2, trace[:-1], trace[1:])),'qty':qty})
    # compute DFG edges (arcs) as pd for all traces using the function get_pairs
    L['arcs'] = list(map(lambda trace, qty: get_pairs(trace, qty), L['trace_full'], L['qty']))
    # merge and aggregate all DFG nodes with sorting in descending frequency
    DFG_arcs = pd.concat([L.iloc[i]['arcs'] for i in list(L.index)])
    DFG_arcs_agg = pd.DataFrame(DFG_arcs.groupby(['pair']).sum()).sort_values(by=['qty'], ascending=False).reset_index()
    
    return DFG_nodes_agg, DFG_arcs_agg

def get_vDFG(DFG_arcs, DFG_nodes, DFG_orientation,S,E):
    '''
    Creating the DFG by Graphviz 

    Parameters
    ----------
    DFG_arcs : pandas.DataFrame
        table with arcs (2 columns: 'pair' - arcs, 'qty' - their frequencies in the event log)
    DFG_nodes : pandas.DataFrame
        table with nodes (2 columns: 'act' - activities, 'qty' - their frequencies in the event log)
    DFG_orientation : str
        'LR' or 'TB' (left -> right or top -> bottom)
    S : str
        symbol for the artificial activity 'Start'- 'I'
    E : str
        symbol for the artificial activity 'End'- 'O'

    Returns
    -------
    <class 'bytes'>
        vDFG.pipe() for vizualization by st.image(vDFG)
    Example
    -------
    vDFG = get_vDFG(DFG_arcs, DFG_nodes, dfg_orientation,'I','O')
    '''
    # init graph
    vDFG = graphviz.Digraph('finite_state_machine')
    vDFG.attr(rankdir = DFG_orientation, size = '1000,1000') 
    vDFG.format = 'png'
    # DFG NODES 
    for i in DFG_nodes.index:
        # start or end - double circles
        if (DFG_nodes['act'].loc[i] == S)|(DFG_nodes['act'].loc[i] == E):
            vDFG.attr('node', shape='doublecircle')
            vDFG.node(DFG_nodes['act'].loc[i], label = DFG_nodes['act'].loc[i])
        else:
            vDFG.attr('node', shape='circle')
            vDFG.node(DFG_nodes['act'].loc[i], label = DFG_nodes['act'].loc[i])
    # DFG EDGES 
    for j in DFG_arcs.index:
        vDFG.edge(DFG_arcs['pair'].loc[j][0], DFG_arcs['pair'].loc[j][1], label = str(DFG_arcs['qty'].loc[j]))
    return vDFG.pipe()

# =============================================================================
# Exercise #2 - DFG matrix & footprint
# =============================================================================
# in_pairs = ['Sa','eE',...], S = "S", E = "E" or ("X","Y") or ("I","O"), in_qty_list = [10,20,...]
def get_footprint_matrix(in_pairs,in_qty_list,S,E):
    '''
    Computing the alternative DFG representations:
    - matrix with frequencis of arcs, 
    - footprint with relations between activities.

    Parameters
    ----------
    in_pairs : list
        list of arcs, i.e. in_pairs = ['Sa','eE']
    in_qty_list : list
        list of frequencies of arcs  (e.g. in_qty_list = [45,42] )
    S : str
        Start symbol (e.g. S = 'I')
    E : str
        Start symbol (e.g. E = 'O')

    Returns
    -------
    df_footprint : pandas.DataFrame
        table with relations between activities (columns and rows - [I,a,b,...,O])
    dict_footprint : dict
        footprint as a dictionary (i.e. dict_footprint['ab'] can returns string '||')
    df_dfg_matrix : pandas.DataFrame
        table with frequencies of arcs between activities (columns and rows - [I,a,b,...,O])
    dict_dfg_matrix : dict
        matrix as a dictionary (i.e. dict_dfg_matrix['ab'] can returns the number 23)

    '''
    # function to get relation between activities in pair
    get_rel = lambda pair,pairs: "||" if (''.join(list(pair)[::-1])) in pairs else "→"
    # get relation and qty lists
    rel = list(map(lambda ss: get_rel(ss, in_pairs), in_pairs))
    # get reverse pairs/relations
    in_pairs_reverse = list(map(lambda ss: ''.join(list(ss)[::-1]), in_pairs))
    rel_reverse = list(map(lambda ss: "||" if (ss == "||") else "←", rel))
    # get full df with index = pairs & rel - relation plus transform it to dict
    arcs_full = pd.DataFrame({'rel':rel+rel_reverse}, index = in_pairs+in_pairs_reverse)
    arcs_dict = arcs_full['rel'].to_dict()
    # get dict pair - qty 
    pair_qty_dict = pd.DataFrame({'qty':in_qty_list}, index = in_pairs)['qty'].to_dict()
    # get sorted activity list
    act_nodes = list(set(list(''.join(in_pairs).replace(S,'').replace(E,'')))) # without S, E
    act_sorted = [S]+sorted(act_nodes)+[E]
    # get the result df
    df_footprint = pd.DataFrame(index = act_sorted)
    df_dfg_matrix = pd.DataFrame(index = act_sorted)
    for col in act_sorted:
        df_footprint[col] = list(map(lambda ss: 
                                     arcs_dict[ss+col] if (ss+col) in list(arcs_full.index) else '#', act_sorted))
        df_dfg_matrix[col] = list(map(lambda ss: pair_qty_dict[ss+col] if (ss+col) in in_pairs else 0, act_sorted))
    # get footprint dict
    all_arcs = [''.join(list(s)) for s in list(itertools.product(act_sorted,act_sorted))]
    other_arcs = list(set(all_arcs) - set(arcs_full.index))   # dict with ''#''
    dict_footprint = {ss: '#' for ss in other_arcs} | arcs_dict  # merge two dicts
    dict_dfg_matrix = {ss: 0 for ss in other_arcs} | pair_qty_dict  # merge two dicts
    return df_footprint, dict_footprint, df_dfg_matrix, dict_dfg_matrix

# =============================================================================
# Special function to get texts in markdown format
# =============================================================================
def get_default_event_log(L):
    if   L == 'L1': return '[<abce>50,<acbe>40,<abcdbce>30,<acbdbce>20,<abcdcbe>10,<acbdcbdbce>10]'
    elif L == 'L2': return '[<aceg>2, <aecg>3,<bdfg>2,<bfdg>4]'
    elif L == 'L3': return '[<acd>45, <bce>42]'
    elif L == 'L4': return '[<abab>5, <ac>2]'
    elif L == 'L5': return '[<abce>10,<acbe>5,<ade>1]' 
    elif L == 'L6': return '[<ab>35, <ba>15]'
    elif L == 'L7': return '[<a>10, <ab>8,<acb>6,<accb>3,<acccb>1]'
    elif L == 'L8': return '[<abef>2,<abecdbf>3,<abcedbf>2,<abcdebf>4,<aebcdbf>3]'
    else: return '[<abce>50,<acbe>40,<abcdbce>30,<acbdbce>20,<abcdcbe>10,<acbdcbdbce>10]'
    
def get_dict_text():
    dict_text = dict()
    # left block
    dict_text['left_block_author_refs','en'] = (''' 
           A streamlit web app "Process Mining training"      
           Module "Directly-Follows Graph (DFG)"      
           v1.0.2 (2023)     
                
           Developed by Alexander Tolmachev (axtolm@gmail.com)    
           
           References   
           1. van der Aalst, W.M.P.: Foundations of Process Discovery. 
           In: van der Aalst, W.M.P., Carmona, J. (eds.) PMSS 2022. 
           LNBIP, vol. 448, pp. 37–75. Springer, Cham (2022). 
           [link](https://doi.org/10.1007/978-3-031-08848-3_2)
           ''')
    # common block
    dict_text['cb_recall_dfg_def','en'] = ('''
           First, let us recall **the definition of a Directly-Follows Graph** [1].
           This definition will be helpful in all exercises.    
           ''')       
    dict_text['cb_dfg_definition','en'] = ('''
           *A Directly-Follows Graph (DFG) is a pair $G=(A,F)$ where* 
           - *$A \subseteq U_{act}$ is a set of activities, and* 
           - *$F \in B((A × A) \cup (\{I\} × A) \cup (A × \{O\}) \cup (\{I\} × \{O\}))$ is a multiset of arcs.*\n 
           *$I$ is the start node and $O$ is the end node $(\{I,O\} \cap U_{act} = \oslash)$*. 
           *$U_{G} \subseteq U_{M}$ is the set of all DFGs*.                       
           ''') 
    dict_text['cb_contents','en'] = ('''              
               In all our exercises, we can use one of the pre-installed simple event logs or create our own. 
               
               **Exercise #1 (Baseline Discovery Algorithm)**.     
               We will use the chosen event log to apply the Baseline Discovery Algorithm and create the Directly-Follows Graph.     
                   
               **Exercise #2 (DFG matrix and footprint)**.      
               We will learn how to obtain a matrix representation of the DFG and build a matrix of relations 
               between the DFG activities using the DFG computed in Exercise #1.

               **To simplify the process model and capture only the dominant behavior, we will consider three types of filtering**:
                   
               **Exercise #3 (Activity-Based Filtering)**.     
               The technique is based on projecting the event log on a subset of activities 
               (here, it means deleting the least frequent activities).    
                   
               **Exercise #4 (Variant-Based Filtering)**.    
               This approach involves deleting selected traces from the event log 
               (here, the least frequent variants).    
                   
               **Exercise #5 (Arc-Based Filtering)**.    
               This method removes the selected arcs in the DFG 
               (here, arcs with a frequency below the specified threshold).
               ''') 
           
    dict_text['common_block','en'] = ('''
           Select an event log from the pre-installed options or create your own.
           Check the event log in tabular form and click the button to study the algorithm step by step.
           ''')     
    dict_text['log_list','en'] = ('''
           $L_1 = [<a,b,c,e>^{50},<a,c,b,e>^{40},<a,b,c,d,b,c,e>^{30},<a,c,b,d,b,c,e>^{20},<a,b,c,d,c,b,e>^{10},<a,c,b,d,c,b,d,b,c,e>^{10}]$,     
           $L_2 = [<a,c,e,g>^{2},<a,e,c,g>^{3},<b,d,f,g>^{2},<b,f,d,g>^{4}]$,     $L_3 = [<a,c,d>^{45},<b,c,e>^{42}]$,   $L_4 = [<a,b,a,b>^{5},<a,c>^{2}]$,       
           $L_5 = [<a,b,c,e>^{10},<a,c,b,e>^{5},<a,d,e>^{1}]$,   $L_6 = [<a,b>^{35},<b,a>^{15}]$,   $L_7 = [<a>^{10},<a,b>^{8},<a,c,b>^{6},<a,c,c,b>^{6},<a,c,c,c,b>^{6}]$,     
           $L_8 = [<a,b,e,f>^{2},<a,b,e,c,d,b,f>^{3},<a,b,c,e,d,b,f>^{2},<a,b,c,d,e,b,f>^{4},<a,e,b,c,d,b,f>^{3}]$
           ''') 
    dict_text['user_log_format_requirements','en'] = ('''
           Use the traditional format of a simple event log: 
           `[<acd>45, <bce>42]`, where `<acd>` is the trace, 
           and `45` is the number of times this trace appears in the event log
           ''')   
    # page 1 - DFG (Baseline Discovery Algorithm)  
    
    dict_text['p1_recall_disc_dfg_def','en'] = ('''                                             
           To construct a DFG based on a simple event log, we need to recall the definition of a Baseline Discovery Algorithm [1].                                               
           ''')                  
    dict_text['p1_discovery_dfg_definition','en'] = ('''
           *Let $L \in B(U_{act}^*)$ be an event log. $disc_{DFG}(L) = (A,F)$ is the DFG based on $L$ with:*
           - *$A = \{a \in \sigma | \sigma \in L\}$, and*
           - *$F = [(\sigma_{i},\sigma_{i+1}) | \sigma \in L\'  \wedge 1 \leq i < |\sigma|]$* 
                   *with $L\' = [<I> ^{.} \sigma ^{.} <O> | \sigma \in L]$*                             
           ''')                                         
    dict_text['p1_step_1_add_I_O','en'] = ('''
           Since the event log does not contain `Start (I)` and `End (O)` nodes, we need to add ones to all traces (Step 1).    
               
           **STEP 1. Add `(I)` and `(O)` to all traces**     
           ''') 
    dict_text['p1_step_1_algorithm','en'] = ('''
           $<a,b,c,e>^{5}$ $→$ $<I,a,b,c,e,O>^{5}$
           ''')        
    dict_text['p1_step_2_3_intro','en'] = ('''
           By definition, it is necessary to find in the event log 
           all activities $A$ (Step 2) and all arcs $F$ (Step 3) connecting them.   
           We can slightly extend the definition and calculate frequencies of $A$ and $F$ in the log.    
           ''')
    dict_text['p1_step_2_title','en'] = ('''
           **STEP 2. Get all activities $A$ and their frequencies (sorted in descending frequency)**    
           ''')
    dict_text['p1_step_2_algorithm','en'] = ('''      
           1. Split each trace into activities with their frequencies:   
           $<I,a,b,O>^{5}$ $→$ $[(I,5),(a,5),(b,5),(O,5)]$     
           $<I,a,c,O>^{2}$ $→$ $[(I,2),(a,2),(c,2),(O,5)]$    
                           
           1. Merge pairs (activity, frequency) from all traces    
           $[(I,5),(a,5),(b,5),(O,5),(I,2),(a,2),(c,2),(O,5)]$
                
           1. Aggregate all pairs and calculate the cumulative frequency for each of them    
           $[(I,7),(a,7),(b,5),(c,2),(O,7)]$
                
           1. Sort pairs in descending frequency    
           $[(I,7),(O,7),(a,7),(b,5),(c,2)]$
           ''')
    dict_text['p1_step_3_title','en'] = ('''
           **STEP 3. Get all arcs $F$ and their frequencies  (sorted in descending frequency)** 
           ''')
    dict_text['p1_step_3_algorithm','en'] = ('''  
           1. Split each trace into arcs (pairs of activities) with their frequencies    
           $<I,a,b,O>^{5}$ $→$ $[((I,a),5),((a,b),5),((b,O),5)]$    
           $<I,a,c,O>^{2}$ $→$ $[((I,a),2),((a,c),2),((c,O),2)]$    
           
           1. Merge pairs (arc, frequency) from all traces     
           $[((I,a),5),((a,b),5),((b,O),5),((I,a),2),((a,c),2),((c,O),2)]$    
           
           1. Aggregate all pairs and calculate the cumulative frequency for each of them     
           $[((I,a),7),((a,b),5),((b,O),5),((a,c),2),((c,O),2)]$     
           
           1. Sort pairs in descending frequency     
           $[((I,a),7),((a,b),5),((b,O),5),((a,c),2),((c,O),2)]$                     
           ''')                  
    dict_text['p1_step_4_title','en'] = ('''
           **STEP 4. DFG visualization by `graphviz`**
           ''')
    dict_text['p1_step_4_summary','en'] = ('''
           Based on the algorithm for constructing the directly-follows graph, we can see that the model 
           takes into account all the activities in the event log and all the direct ordering relationships between them.
           1. This provides good fitness when all traces in the log can be replayed by the model from beginning to end.
           2. Modeling parallelism leads to the formation of cycles and to the directly-follows graph reproducing behavior that is not present in the event log.
           3. The directly-follows graph may become difficult to comprehend due to the large number of arcs in the graph (a spaghetti-like model).
           ''')           
    dict_text['p1_step_1_2_3_4_summary','en'] = ('''
               **Success! We have accomplished the following:**
                1. Added (I) and (O) to all traces.
                2. Obtained all activities and their frequencies in A.
                3. Obtained all arcs and their frequencies in F.
                4. Visualized DFG using `graphviz`."                                   
               ''') 
    # =============================================================================
    # page 2 - DFG matrix & footprint
    # =============================================================================
    dict_text['p2_step_1_title','en'] = ('''
               **Step 1. Get the DFG matrix**                              
           ''')                                             
    dict_text['p2_dfg_matrix_intro','en'] = ('''
               Besides being represented as two tables (one with activities and their frequencies, 
               and the other with arcs and their frequencies), the directly-follows graph (DFG) can also be represented as a matrix [1].    
           ''')
    dict_text['p2_step_1_algorithm','en'] = ('''
               1. We have the DFG represented by two multisets: $A = [(a,12),(b,10),(I,7),(O,7),(c,2)]$ and $F=[((a,b),10),((I,a),7),((b,O),5),((b,a),5),((a,c),2),((c,O),2)]$                   
               2. Construct a square matrix $M$ with rows labeled as $[I,a,b,c,O]$ and columns labeled as $[I,a,b,c,O]$.
               3. Initialize all elements of matrix $M$ to $0$.    
               
               ||I|a|b|c|O|   
               |--|--|--|--|--|--|   
               |**I**|0|0|0|0|0|
               |**a**|0|0|0|0|0|
               |**b**|0|0|0|0|0|
               |**c**|0|0|0|0|0|
               |**O**|0|0|0|0|0|   
               
               4. Modify matrix $M$ using the values from $F$: set $(a,b)$ to $10$, $(I,a)$ to $7$, $(b,O)$ to $5$, $(b,a)$ to $5$, $(a,c)$ to $2$, $(c,O)$ to $2$,     
               where $(a,b)$ represents an element of the DFG matrix located in row $a$ and column $b$.    
               
               ||I|a|b|c|O|   
               |--|--|--|--|--|--|   
               |**I**|0|**7**|0|0|0|
               |**a**|0|0|**10**|**2**|0|
               |**b**|0|**5**|0|0|**5**|
               |**c**|0|0|0|0|**2**|
               |**O**|0|0|0|0|0|     
               
           ''')  
    dict_text['p2_step_2_title','en'] = ('''
                      **Step 2. Get the DFG footprint**                              
           ''') 
    dict_text['p2_dfg_matrix_comment','en'] = ('''
               While matrix representation can be convenient for visualizing small DFGs, 
               it may not be efficient for large graphs since the matrix can be highly sparse, containing many zeros.     
               To save space, we only store the non-zero elements in the table.
           ''')    
    dict_text['p2_dfg_footprint_intro','en'] = ('''
              The DFG footprint captures the relations between activities based on the following definition [1].     
           ''')                                                     
    dict_text['p2_dfg_footprint_definition','en'] = ('''
           *Let $G = (A, F) \in U_G$ be a DFG.*     
           *$G$ defines a footprint $fp(G) \in (A'$x$A') → \{→,←,\|,\#\}$ such that $A' = A \cup \{I,O\}$ and for any $(a_1, a_2) \in A'$x$A'$:*   
            - *$fp(G)((a_1,a_2)) =$ "$→$" if $(a_1,a_2) \in F$ and $(a_2,a_1)$ $\\notin$ $F$,*   
            - *$fp(G)((a_1,a_2)) =$ "$←$" if $(a_1,a_2) \\notin F$ and $(a_2,a_1) \in F$,*    
            - *$fp(G)((a_1,a_2)) =$ "$\|$" if $(a_1,a_2) \in F$ and $(a_2,a_1) \in F$, and*     
            - *$fp(G)((a_1,a_2)) =$ "$\#$" if $(a_1,a_2) \\notin F$ and $(a_2,a_1) \\notin F$*.    
           ''')   
    dict_text['p2_step_2_algorithm','en'] = ('''
               1. We have the DFG represented by two multisets: $A = [(a,12),(b,10),(I,7),(O,7),(c,2)]$ and $F=[((a,b),10),((I,a),7),((b,O),5),((b,a),5),((a,c),2),((c,O),2)]$                   
               2. Construct a square matrix $M$ with rows labeled as $[I,a,b,c,O]$ and columns labeled as $[I,a,b,c,O]$.
               3. Initialize all elements of matrix $M$ to $\#$.    
                
                ||I|a|b|c|O|   
                |--|--|--|--|--|--|   
                |**I**|#|#|#|#|#|
                |**a**|#|#|#|#|#|
                |**b**|#|#|#|#|#|
                |**c**|#|#|#|#|#|
                |**O**|#|#|#|#|#|   
                
                4. Modify matrix $M$ using the following rules for each arc in $F$:     
                   if $(a_1,a_2) \in F \wedge (a_2,a_1) \in F$: set $(a_1,a_2)$ to "$\|$",      
                   in our case we have to set $(a,b)$ to "$\|$" and $(b,a)$ to "$\|$",        
                   
                   if $(a_1,a_2) \in F \wedge (a_2,a_1) \\notin F$: set $(a_1,a_2)$ to "$→$" and $(a_2,a_1)$ to "$←$",      
                   in our case we have to set    
                   $(I,a)$ to "$→$" and $(a,I)$ to "$←$",    
                   $(a,c)$ to "$→$" and $(c,a)$ to "$←$",     
                   $(b,O)$ to "$→$" and $(O,b)$ to "$←$",      
                   $(c,O)$ to "$→$" and $(O,c)$ to "$←$".      
                                  
                ||I|a|b|c|O|   
                |--|--|--|--|--|--|   
                |**I**|#|**→**|#|#|#|
                |**a**|**←**|#|**\|\|**|**→**|#|
                |**b**|#|**\|\|**|#|#|**→**|
                |**c**|#|**←**|#|#|**→**|
                |**O**|#|#|**←**|**←**|#|     
               
           ''')     
    dict_text['p2_dfg_footprint_summary','en'] = ('''
           Between two activities $a_1$ and $a_2$, precisely one of four possible relations holds [1]:
           - $a_1$ $→$ $a_2$ (i.e., $a_1$ is sometimes directly followed by $a_2$, but $a_2$ is never directly followed by $a_1$),   
           - $a_1$ $←$ $a_2$ (i.e., $a_2$ is sometimes directly followed by $a_1$, but $a_1$ is never directly followed by $a_2$),
           - $a_1$ $\|$ $a_2$ (i.e., $a_1$ is sometimes directly followed by $a_2$ and $a_2$ is sometimes directly followed by $a_1$), and   
           - $a_1$ $\#$ $a_2$ (i.e., $a_1$ is never directly followed by $a_2$ and $a_2$ is never directly followed by $a_1$).                                      
           ''')  
    dict_text['p2_step_1_2_summary','en'] = ('''
               **Success! We have completed the following steps:**
               1. Obtained the DFG matrix.
               2. Obtained the DFG footprint.         
               ''')      
    # =============================================================================
    # page 3 - Activity-Based Filtering 
    # =============================================================================
    dict_text['p3_abf_definition_intro','en'] = ('''
              Let us recall the definition of Activity-Based Filtering [1].   
              ''')
    dict_text['p3_abf_definition','en'] = ('''
              *Let $L \in B(U_{act}^*)$ be an event log and $\\tau_{act} \in N$.*     
              *$filter^{act}(L,\\tau_{act})$ = $L \\uparrow _A$ with $A = \{a \in act(L) | \#^{act}_{L}(a) \geq  \\tau_{act}\}$, where*    
              - $act(L) = \{a \in \\sigma | \\sigma \in L \}$ are the activities in event log $L$,    
              - $\#^{act}_{L}(a) = \sum_{\sigma \in L} |\{i \in \{1,...,|\sigma| \}|\sigma_i = a \}|$
              *is the frequency of activity $a \in act(L)$ in event log $L$*.    
              - *for a subset of activities $A \\subseteq act(L)$ and trace $\sigma \in L$, we define the projection $\sigma \\uparrow _A$ such that*    
              *$<> \\uparrow _A = <>$ and $(\sigma \\cdot <a>) \\uparrow _A = \sigma \\uparrow _A \\cdot <a>$ if $a \in A$, 
              and $(\sigma \\cdot <a>) \\uparrow _A = \sigma \\uparrow _A$ if $a \\notin A$*,    
              - *$L \\uparrow _A = [\sigma \\uparrow _A | \sigma \in L]$ is the projection of $L$ on a subset of activities $A \\subseteq act(L)$*.        
              ''')
    dict_text['p3_slider_comment','en'] = ('''
              All activities with a frequency $< %s$ will be removed from the event log, but all cases are retained (the trivial trace can be $<I,O>$).
              ''')  
    dict_text['p3_full_a_tab','en'] = ('''
              Full set of activities for filtering
              ''')                
    dict_text['p3_filtered_a_tab','en'] = ('''
              Filtered activities $A$ (frequencies $\geq$ %s)
              ''')     
    dict_text['p3_note_start_end','en'] = ('''
              Note that `I` and `O` are not involved in filtering
              ''')     
    dict_text['p3_step_1_title','en'] = ('''
              **Step 1. Get the projection of $L$ on a subset of filtered activities $A$**
              ''')                               
    dict_text['p3_step_1_example','en'] = ('''
              1. Get projection for each trace in the event log:      
                  $<a,c,b,d,b,c,e>^{5} \\uparrow _{\{b,c\}}$ $→$ $<c,b,b,c>^{5}$    
              2. Add `(I)` and `(O)` to all traces and their projections (this is the first step in the DFG construction):      
                  $<a,c,b,d,b,c,e>^{5}$ $→$ $<I,a,c,b,d,b,c,e,I>^{5}$    
                  $<c,b,b,c>^{5}$ $→$ $<I,c,b,b,c,O>^{5}$
              ''')    
    dict_text['p3_step_2_title','en'] = ('''
              **Step 2. Get DFG nodes and arcs for the $L$ and the projection of $L$ by the Baseline Discovery Algorithm**
              ''')  
    dict_text['p3_step_2_subtitle','en'] = ('''
               You can compare the original $DFG$ based on $L$ and $DFG$ based on the projection of $L$ after the Activity-Based Filtering ($L \\uparrow _A$)
              ''')   
    dict_text['p3_step_2_col1_original_nodes','en'] = ('''
               Original DFG nodes 
              ''')  
    dict_text['p3_step_2_col2_original_arcs','en'] = ('''
               Original DFG arcs
              ''') 
    dict_text['p3_step_2_col3_filtered_nodes','en'] = ('''
               DFG nodes after Activity-Based Filtering
              ''')  
    dict_text['p3_step_2_col4_filtered_arcs','en'] = ('''
               DFG arcs after Activity-Based Filtering
              ''')     
    dict_text['p3_step_2_co1_original_dfg','en'] = ('''
               Original Directly-Follows Graph
              ''') 
    dict_text['p3_step_2_co2_filtered_dfg','en'] = ('''
               Directly-Follows Graph after Activity-Based Filtering
              ''')   
    dict_text['p3_step_1_2_summary','en'] = ('''
               **Success! We have completed the following steps:**
               1. Obtained the projection of L onto a subset of filtered activities A using a threshold of τ(act).
               2. Obtained and compared the DFG nodes and arcs for L and its projection using the Baseline Discovery Algorithm.       
               ''')     
    # =============================================================================
    # page 4 - Variant-Based Filtering 
    # =============================================================================
    dict_text['p4_vbf_definition_intro','en'] = ('''
              Let us recall the definition of Variant-Based Filtering [1].  
              ''')
    dict_text['p4_vbf_definition','en'] = ('''
              *Let $L \in B(U_{act}^*)$ be an event log and $\\tau_{var} \in N$.*     
              *$filter^{var}(L,\\tau_{var})$ = $L \\Uparrow _V$ with $V = \{\sigma \in var(L) | \#^{var}_{L}(\sigma) \geq  \\tau_{var}\}$, where*                                                                               
              - $var(L) = \{\sigma \in L \}$ are the trace variants in event log $L$,    
              - $\#^{var}_{L}(\sigma) = L(\sigma)$
              *is the frequency of variant $\sigma \in var(L)$ in event log $L$*.    
              - *$L \\Uparrow _V = [\sigma \in L | \sigma \in V]$ is the projection of $L$ on a subset of trace variants $V \\subseteq var(L)$*.        
              ''')
    dict_text['p4_slider_comment','en'] = ('''
              All trace variants with a frequency $< %s$ will be removed from the event log.
              ''') 
    dict_text['p4_full_v_tab','en'] = ('''
              All trace variants for filtering (full event log)
              ''') 
    dict_text['p4_filtered_v_tab','en'] = ('''
              Filtered trace variants (frequencies $\geq$ %s)
              ''') 
    dict_text['p4_step_1_title','en'] = ('''
              **Step 1. Get DFG nodes and arcs for the original $L$ and its subset $V$ using the Baseline Discovery Algorithm**
              ''')  
    dict_text['p4_step_1_subtitle','en'] = ('''
               You can compare the original $DFG$ based on $L$ and $DFG$ based on the projection of $L$ after the Variant-Based Filtering ($L \\Uparrow _V$).    
              ''')   
    dict_text['p4_step_1_col1_original_nodes','en'] = ('''
               Original DFG nodes 
              ''')  
    dict_text['p4_step_1_col2_original_arcs','en'] = ('''
               Original DFG arcs
              ''') 
    dict_text['p4_step_1_col3_filtered_nodes','en'] = ('''
               DFG nodes after Variant-Based Filtering
              ''')  
    dict_text['p4_step_1_col4_filtered_arcs','en'] = ('''
               DFG arcs after Variant-Based Filtering
              ''')     
    dict_text['p4_step_1_co1_original_dfg','en'] = ('''
               Original Directly-Follows Graph
              ''') 
    dict_text['p4_step_1_co2_filtered_dfg','en'] = ('''
               Directly-Follows Graph after Variant-Based Filtering
              ''')   
    dict_text['p4_step_1_summary','en'] = ('''
               **Success! We have completed the following steps:**
               1. Filtered the event log traces based on their frequencies using a threshold of $τ_{var}$.
               2. Obtained and compared the DFG nodes and arcs for the original event log $L$ and its subset $V$ using the Baseline Discovery Algorithm.       
               ''')  
    # =============================================================================
    # page 5 - Arc-Based Filtering 
    # =============================================================================
    dict_text['p5_arc_bf_definition_intro','en'] = ('''
               **Let us recall the definition of Arc-Based Filtering [1]**.  
               ''')
    dict_text['p5_arc_bf_definition','en'] = ('''
               *Let $G = (A,F) \in U_G$ be a DFG and $\\tau_{arc} \in N$.*     
               *$filter^{arc}(G,\\tau_{arc}) = (A,F')$ with $F' = [(x,y) \in F | F((x,y)) \geq \\tau_{arc}]$*.        
               ''')
    dict_text['p5_slider_comment','en'] = ('''
              All arcs with a frequency $< %s$ will be removed from the graph.     
              Note that this filter only operates on the DFG and does not modify the original event log.
              ''') 
    dict_text['p5_full_arc_tab','en'] = ('''
              All arcs for filtering (full DFG)
              ''') 
    dict_text['p5_filtered_arc_tab','en'] = ('''
              Filtered arcs (frequencies $\geq$ %s)
              ''') 
    dict_text['p5_step_1_title','en'] = ('''
              **Step 1. Obtain the DFG based on the full multiset of arcs and its filtered subset using the Baseline Discovery Algorithm**
              ''')  
    dict_text['p5_step_1_subtitle','en'] = ('''
               You can compare the original $DFG$ and $DFG$ after the Arc-Based Filtering.    
              ''')   
    dict_text['p5_step_1_col1_original_nodes','en'] = ('''
               Original DFG nodes 
              ''')  
    dict_text['p5_step_1_col2_original_arcs','en'] = ('''
               Original DFG arcs
              ''') 
    dict_text['p5_step_1_col3_filtered_nodes','en'] = ('''
               DFG nodes after Arc-Based Filtering
              ''')  
    dict_text['p5_step_1_col4_filtered_arcs','en'] = ('''
               DFG arcs after Arc-Based Filtering
              ''')     
    dict_text['p5_step_1_co1_original_dfg','en'] = ('''
               Original Directly-Follows Graph
              ''') 
    dict_text['p5_step_1_co2_filtered_dfg','en'] = ('''
               Directly-Follows Graph after Arc-Based Filtering
              ''')   
    dict_text['p5_step_1_pre_summary','en'] = ('''                    
               We could observe that:   
                  a) This filtering only affects the DFG arcs and leaves the event log and DFG nodes unchanged.                      
                  b) The graph can fall apart after removing some arcs.    
                  c) The arc frequencies become uncoordinated with each other after filtering.
               ''')           
    dict_text['p5_step_1_summary','en'] = ('''
               **Success! We have completed the following steps:**
               1. Filtered the DFG arcs based on their frequencies using a threshold of $τ_{arc}$.
               2. Obtained and compared the original $DFG$ and the filtered $DFG$ applying the Arc-Based Filtering algorithm.     
               ''') 
    return dict_text

if __name__ == "__main__":
    main()
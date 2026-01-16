import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv('API_URL', 'http://localhost:5000/api')

# Page config
st.set_page_config(
    page_title="Migration Audit Platform",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e40af;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
    }
    .stAlert {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔍 Migration Audit Platform")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "➕ New Project", "📊 View Results", "📋 Projects List"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "Migration Audit Platform helps you analyze website migrations with "
    "comprehensive URL comparison, SEO validation, performance testing, "
    "and mobile responsiveness checks."
)

# Helper Functions
def api_request(endpoint, method='GET', **kwargs):
    """Make API request with error handling"""
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        if method == 'GET':
            response = requests.get(url, **kwargs)
        elif method == 'POST':
            response = requests.post(url, **kwargs)
        
        if response.status_code in [200, 201]:
            return {'success': True, 'data': response.json()}
        else:
            return {'success': False, 'error': response.json().get('error', 'Unknown error')}
    except Exception as e:
        return {'success': False, 'error': str(e)}

# ==========================================
# HOME PAGE
# ==========================================
if page == "🏠 Home":
    st.markdown('<p class="main-header">🔍 Migration Audit Platform</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Welcome to the Migration Audit Platform
    
    This platform provides comprehensive auditing tools for website migrations, helping you ensure 
    a smooth transition with minimal SEO and performance impact.
    
    ### What We Analyze:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🔗 URL Analysis
        - Direct URL matching
        - Redirect mapping validation
        - Missing URL detection
        - Pattern change analysis
        
        #### 📈 Performance Testing
        - Lighthouse audits
        - Core Web Vitals (LCP, CLS, INP)
        - Page speed comparison
        - Before/after metrics
        """)
    
    with col2:
        st.markdown("""
        #### 🎯 SEO Validation
        - Title tag comparison
        - Meta description matching
        - H1 heading analysis
        - Canonical URL verification
        
        #### 📱 Mobile Responsiveness
        - Multi-viewport testing
        - Layout issue detection
        - Touch target validation
        - Screenshot comparison
        """)
    
    st.markdown("---")
    st.markdown("### Getting Started")
    
    st.info("👈 Use the navigation menu on the left to create a new project or view existing results.")
    
    with st.expander("📖 How It Works"):
        st.markdown("""
        1. **Create Project**: Upload your old and new sitemaps, plus optional GSC data and redirect mapping
        2. **Processing**: The system runs a 10-step audit analyzing URLs, SEO, performance, and mobile responsiveness
        3. **View Results**: Interactive dashboards show comprehensive comparisons and insights
        4. **Export**: Download detailed CSV or JSON reports for further analysis
        
        **Processing Time**: Typically 15-25 minutes depending on the number of URLs
        """)

# ==========================================
# NEW PROJECT PAGE
# ==========================================
elif page == "➕ New Project":
    st.markdown('<p class="main-header">Create New Migration Project</p>', unsafe_allow_html=True)
    
    with st.form("new_project_form", clear_on_submit=False):
        st.subheader("Project Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input(
                "Project Name *",
                placeholder="e.g., My Website Migration",
                help="A friendly name for this migration project"
            )
            old_url = st.text_input(
                "Old Base URL *",
                placeholder="https://old-site.com",
                help="The base URL of your current site"
            )
        
        with col2:
            description = st.text_area(
                "Description",
                height=100,
                placeholder="Optional description of this migration",
                help="Any notes about this migration project"
            )
            new_url = st.text_input(
                "New Base URL *",
                placeholder="https://new-site.com",
                help="The base URL of your new site"
            )
        
        st.markdown("---")
        st.subheader("Upload Files")
        
        col1, col2 = st.columns(2)
        
        with col1:
            old_sitemap = st.file_uploader(
                "Old Sitemap (XML) *",
                type=['xml'],
                help="XML sitemap from your current site"
            )
            gsc_export = st.file_uploader(
                "Google Search Console Export (CSV)",
                type=['csv'],
                help="Optional: GSC performance data for prioritizing URLs"
            )
        
        with col2:
            new_sitemap = st.file_uploader(
                "New Sitemap (XML) *",
                type=['xml'],
                help="XML sitemap from your new site"
            )
            redirects = st.file_uploader(
                "Redirect Mapping (CSV)",
                type=['csv'],
                help="Optional: CSV with OldURL,NewURL redirect mappings"
            )
        
        st.markdown("---")
        submit = st.form_submit_button(
            "🚀 Create Project and Start Analysis",
            use_container_width=True,
            type="primary"
        )
        
        if submit:
            # Validation
            if not all([project_name, old_url, new_url, old_sitemap, new_sitemap]):
                st.error("⚠️ Please fill all required fields (*) and upload both sitemaps")
            else:
                with st.spinner("Creating project and starting analysis..."):
                    # Prepare files
                    files = {
                        'oldSitemap': ('old-sitemap.xml', old_sitemap, 'application/xml'),
                        'newSitemap': ('new-sitemap.xml', new_sitemap, 'application/xml'),
                    }
                    
                    if gsc_export:
                        files['gscExport'] = ('gsc-export.csv', gsc_export, 'text/csv')
                    if redirects:
                        files['redirectMapping'] = ('redirects.csv', redirects, 'text/csv')
                    
                    # Prepare data
                    data = {
                        'projectName': project_name,
                        'description': description,
                        'oldBaseUrl': old_url,
                        'newBaseUrl': new_url
                    }
                    
                    # Create project
                    create_response = api_request('migration-projects', method='POST', files=files, data=data)
                    
                    if create_response['success']:
                        project = create_response['data']['project']
                        project_id = project['_id']
                        
                        st.success(f"✅ Project created successfully!")
                        st.info(f"**Project ID**: `{project_id}`")
                        
                        # Start processing
                        process_response = api_request(f'migration-projects/{project_id}/process', method='POST')
                        
                        if process_response['success']:
                            st.success("🚀 Analysis started! Processing will take approximately 15-25 minutes.")
                            st.balloons()
                            
                            # Save to session state
                            st.session_state['current_project_id'] = project_id
                            st.session_state['project_name'] = project_name
                            
                            st.markdown("---")
                            st.markdown("### Next Steps:")
                            st.markdown(f"""
                            1. **Copy your Project ID**: `{project_id}`
                            2. Go to **📊 View Results** page
                            3. Enter your Project ID to track progress
                            4. Refresh periodically to see real-time updates
                            """)
                            
                            if st.button("📊 Go to Results Page"):
                                st.rerun()
                        else:
                            st.error(f"❌ Failed to start processing: {process_response['error']}")
                    else:
                        st.error(f"❌ Failed to create project: {create_response['error']}")

# ==========================================
# VIEW RESULTS PAGE
# ==========================================
elif page == "📊 View Results":
    st.markdown('<p class="main-header">Migration Audit Results</p>', unsafe_allow_html=True)
    
    # Project ID input
    col1, col2 = st.columns([3, 1])
    with col1:
        project_id = st.text_input(
            "Enter Project ID",
            value=st.session_state.get('current_project_id', ''),
            placeholder="Enter your project ID here",
            help="The ID you received when creating the project"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        load_btn = st.button("🔄 Load Results", type="primary", use_container_width=True)
    
    if (load_btn or project_id) and project_id:
        # Fetch project status
        status_response = api_request(f'migration-projects/{project_id}/status')
        
        if status_response['success']:
            status = status_response['data']
            
            # Display project info
            st.markdown("### Project Information")
            info_col1, info_col2 = st.columns(2)
            with info_col1:
                st.markdown(f"**Project Name**: {status.get('projectName', 'N/A')}")
                st.markdown(f"**Old Site**: {status.get('oldBaseUrl', 'N/A')}")
            with info_col2:
                st.markdown(f"**Status**: {status['status'].upper()}")
                st.markdown(f"**New Site**: {status.get('newBaseUrl', 'N/A')}")
            
            st.markdown("---")
            
            # Display status metrics
            st.markdown("### Processing Status")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                status_color = {
                    'pending': '🟡',
                    'processing': '🔵',
                    'completed': '🟢',
                    'failed': '🔴'
                }.get(status['status'], '⚪')
                st.metric("Status", f"{status_color} {status['status'].upper()}")
            
            with col2:
                progress = status['processingStatus']['progress']
                st.metric("Progress", f"{progress}%")
            
            with col3:
                stage = status['processingStatus']['stage'].replace('_', ' ').title()
                st.metric("Current Stage", stage)
            
            # Progress bar
            st.progress(progress / 100)
            
            # If completed, show full results
            if status['status'] == 'completed':
                st.markdown("---")
                
                # Fetch full results
                results_response = api_request(f'migration-projects/{project_id}/results')
                
                if results_response['success']:
                    data = results_response['data']
                    results = data['results']
                    
                    # === OVERVIEW METRICS ===
                    st.markdown("## 📊 Overview")
                    
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        url_summary = results.get('urlComparison', {}).get('summary', {})
                        total_urls = url_summary.get('totalOldUrls', 0)
                        match_rate = url_summary.get('matchRate', 0)
                        st.metric(
                            "Total URLs",
                            f"{total_urls:,}",
                            delta=f"{match_rate}% matched",
                            delta_color="normal"
                        )
                    
                    with metric_col2:
                        perf_summary = results.get('performanceValidation', {}).get('summary', {})
                        new_score = perf_summary.get('avgScoreNew', 0)
                        score_delta = perf_summary.get('avgScoreDelta', 0)
                        st.metric(
                            "Avg Performance",
                            f"{new_score}/100",
                            delta=f"{score_delta:+.0f} points",
                            delta_color="normal" if score_delta >= 0 else "inverse"
                        )
                    
                    with metric_col3:
                        seo_summary = results.get('seoValidation', {}).get('summary', {})
                        seo_score = seo_summary.get('avgMatchScore', 0)
                        st.metric(
                            "SEO Health",
                            f"{seo_score:.0f}%",
                            delta="Match score"
                        )
                    
                    with metric_col4:
                        mobile_summary = results.get('mobileResponsiveness', {}).get('summary', {})
                        new_mobile = mobile_summary.get('new', {})
                        responsive = new_mobile.get('fullyResponsive', 0)
                        total_tested = new_mobile.get('totalTested', 0)
                        st.metric(
                            "Mobile Ready",
                            f"{responsive}/{total_tested}",
                            delta=f"{(responsive/total_tested*100) if total_tested > 0 else 0:.0f}% responsive"
                        )
                    
                    st.markdown("---")
                    
                    # === VISUALIZATIONS ===
                    st.markdown("## 📈 Visualizations")
                    
                    tab1, tab2, tab3, tab4 = st.tabs([
                        "🔗 URL Distribution",
                        "⚡ Performance",
                        "🎯 SEO Scores",
                        "📱 Mobile"
                    ])
                    
                    with tab1:
                        if results.get('urlComparison'):
                            url_data = results['urlComparison']['summary']
                            
                            col_a, col_b = st.columns([2, 1])
                            
                            with col_a:
                                # Pie chart
                                fig = go.Figure(data=[go.Pie(
                                    labels=['Matched', 'Redirected', 'Missing', 'New'],
                                    values=[
                                        url_data.get('matchedCount', 0),
                                        url_data.get('redirectedCount', 0),
                                        url_data.get('missingCount', 0),
                                        len(results['urlComparison'].get('newOnly', []))
                                    ],
                                    marker=dict(colors=['#10b981', '#f59e0b', '#ef4444', '#3b82f6']),
                                    hole=0.4,
                                    textinfo='label+percent+value',
                                    textposition='outside'
                                )])
                                fig.update_layout(
                                    title="URL Status Distribution",
                                    height=400
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col_b:
                                st.markdown("#### Summary")
                                st.markdown(f"""
                                - **Total Old URLs**: {url_data.get('totalOldUrls', 0):,}
                                - **Total New URLs**: {url_data.get('totalNewUrls', 0):,}
                                - **Match Rate**: {url_data.get('matchRate', 0):.1f}%
                                - **Matched**: {url_data.get('matchedCount', 0):,}
                                - **Redirected**: {url_data.get('redirectedCount', 0):,}
                                - **Missing**: {url_data.get('missingCount', 0):,}
                                """)
                    
                    with tab2:
                        if results.get('performanceValidation'):
                            perf_data = results['performanceValidation'].get('comparisons', [])[:10]
                            
                            if perf_data:
                                df = pd.DataFrame([
                                    {
                                        'URL': p['url'][:30] + '...' if len(p['url']) > 30 else p['url'],
                                        'Old Score': p['oldScore'],
                                        'New Score': p['newScore'],
                                        'Delta': p['scoreDelta']
                                    }
                                    for p in perf_data
                                ])
                                
                                fig = go.Figure()
                                fig.add_trace(go.Bar(
                                    name='Old Site',
                                    x=df['URL'],
                                    y=df['Old Score'],
                                    marker_color='#ef4444',
                                    text=df['Old Score'],
                                    textposition='outside'
                                ))
                                fig.add_trace(go.Bar(
                                    name='New Site',
                                    x=df['URL'],
                                    y=df['New Score'],
                                    marker_color='#10b981',
                                    text=df['New Score'],
                                    textposition='outside'
                                ))
                                fig.update_layout(
                                    title="Performance Scores Comparison (Top 10 URLs)",
                                    barmode='group',
                                    xaxis_tickangle=-45,
                                    yaxis=dict(range=[0, 100]),
                                    height=500
                                )
                                st.plotly_chart(fig, use_container_width=True)
                                
                                # Core Web Vitals
                                st.markdown("#### Core Web Vitals")
                                cwv_col1, cwv_col2, cwv_col3 = st.columns(3)
                                
                                avg_lcp_old = sum(p['coreWebVitals']['lcp']['old'] for p in perf_data) / len(perf_data)
                                avg_lcp_new = sum(p['coreWebVitals']['lcp']['new'] for p in perf_data) / len(perf_data)
                                
                                with cwv_col1:
                                    st.metric("Avg LCP", f"{avg_lcp_new:.0f}ms", delta=f"{avg_lcp_new - avg_lcp_old:.0f}ms", delta_color="inverse")
                                
                                avg_cls_old = sum(p['coreWebVitals']['cls']['old'] for p in perf_data) / len(perf_data)
                                avg_cls_new = sum(p['coreWebVitals']['cls']['new'] for p in perf_data) / len(perf_data)
                                
                                with cwv_col2:
                                    st.metric("Avg CLS", f"{avg_cls_new:.3f}", delta=f"{avg_cls_new - avg_cls_old:.3f}", delta_color="inverse")
                                
                                avg_inp_old = sum(p['coreWebVitals']['inp']['old'] for p in perf_data) / len(perf_data)
                                avg_inp_new = sum(p['coreWebVitals']['inp']['new'] for p in perf_data) / len(perf_data)
                                
                                with cwv_col3:
                                    st.metric("Avg INP", f"{avg_inp_new:.0f}ms", delta=f"{avg_inp_new - avg_inp_old:.0f}ms", delta_color="inverse")
                    
                    with tab3:
                        if results.get('seoValidation'):
                            seo_data = results['seoValidation'].get('comparisons', [])[:15]
                            
                            if seo_data:
                                df = pd.DataFrame([
                                    {
                                        'URL': s['oldUrl'][:40] + '...' if len(s['oldUrl']) > 40 else s['oldUrl'],
                                        'Match Score': s['matchScore'],
                                        'Severity': s['severity']
                                    }
                                    for s in seo_data
                                ])
                                
                                fig = px.bar(
                                    df,
                                    x='URL',
                                    y='Match Score',
                                    color='Match Score',
                                    color_continuous_scale='RdYlGn',
                                    range_color=[0, 100],
                                    title="SEO Match Scores (Top 15 URLs)",
                                    text='Match Score'
                                )
                                fig.update_layout(
                                    xaxis_tickangle=-45,
                                    height=500
                                )
                                fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
                                st.plotly_chart(fig, use_container_width=True)
                                
                                # Summary stats
                                perfect = sum(1 for s in seo_data if s['matchScore'] >= 95)
                                good = sum(1 for s in seo_data if 80 <= s['matchScore'] < 95)
                                needs_work = sum(1 for s in seo_data if s['matchScore'] < 80)
                                
                                sum_col1, sum_col2, sum_col3 = st.columns(3)
                                with sum_col1:
                                    st.metric("Perfect Matches", f"{perfect}/{len(seo_data)}")
                                with sum_col2:
                                    st.metric("Good Matches", f"{good}/{len(seo_data)}")
                                with sum_col3:
                                    st.metric("Needs Work", f"{needs_work}/{len(seo_data)}")
                    
                    with tab4:
                        if results.get('mobileResponsiveness'):
                            mobile_data = results['mobileResponsiveness']['summary']
                            
                            comparison_data = {
                                'Category': ['Fully Responsive', 'Minor Issues', 'Major Issues'],
                                'Old Site': [
                                    mobile_data['old'].get('fullyResponsive', 0),
                                    mobile_data['old'].get('hasMinorIssues', 0),
                                    mobile_data['old'].get('hasMajorIssues', 0)
                                ],
                                'New Site': [
                                    mobile_data['new'].get('fullyResponsive', 0),
                                    mobile_data['new'].get('hasMinorIssues', 0),
                                    mobile_data['new'].get('hasMajorIssues', 0)
                                ]
                            }
                            
                            fig = go.Figure()
                            fig.add_trace(go.Bar(
                                name='Old Site',
                                x=comparison_data['Category'],
                                y=comparison_data['Old Site'],
                                marker_color='#ef4444',
                                text=comparison_data['Old Site'],
                                textposition='outside'
                            ))
                            fig.add_trace(go.Bar(
                                name='New Site',
                                x=comparison_data['Category'],
                                y=comparison_data['New Site'],
                                marker_color='#10b981',
                                text=comparison_data['New Site'],
                                textposition='outside'
                            ))
                            fig.update_layout(
                                title="Mobile Responsiveness Comparison",
                                barmode='group',
                                height=400
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Mobile insights
                            st.markdown("#### Mobile Insights")
                            if mobile_data.get('improved', 0) > 0:
                                st.success(f"✅ {mobile_data['improved']} pages improved in mobile responsiveness")
                            if mobile_data.get('regressed', 0) > 0:
                                st.warning(f"⚠️ {mobile_data['regressed']} pages regressed in mobile responsiveness")
                    
                    st.markdown("---")
                    
                    # === DETAILED RESULTS ===
                    st.markdown("## 📋 Detailed Results")
                    
                    with st.expander("🔗 URL Comparison Details", expanded=False):
                        if results.get('urlComparison'):
                            url_tab1, url_tab2, url_tab3 = st.tabs(["Matched", "Missing", "Redirected"])
                            
                            with url_tab1:
                                matched = results['urlComparison'].get('matched', [])[:100]
                                if matched:
                                    df = pd.DataFrame(matched)
                                    st.dataframe(df[['oldUrl', 'newUrl']], use_container_width=True)
                                else:
                                    st.info("No matched URLs")
                            
                            with url_tab2:
                                missing = results['urlComparison'].get('missing', [])[:50]
                                if missing:
                                    df = pd.DataFrame(missing)
                                    st.dataframe(df, use_container_width=True)
                                    st.warning(f"⚠️ {len(missing)} URLs are missing - potential 404s!")
                                else:
                                    st.success("✅ No missing URLs")
                            
                            with url_tab3:
                                redirected = results['urlComparison'].get('redirected', [])[:50]
                                if redirected:
                                    df = pd.DataFrame(redirected)
                                    st.dataframe(df[['oldUrl', 'newUrl']], use_container_width=True)
                                else:
                                    st.info("No redirected URLs")
                    
                    with st.expander("🎯 SEO Validation Details", expanded=False):
                        if results.get('seoValidation'):
                            seo_comparisons = results['seoValidation'].get('comparisons', [])[:50]
                            if seo_comparisons:
                                df = pd.DataFrame([
                                    {
                                        'URL': c['oldUrl'],
                                        'Match Score': f"{c['matchScore']}%",
                                        'Title Match': '✅' if c['title']['match'] else '❌',
                                        'Desc Match': '✅' if c['description']['match'] else '❌',
                                        'H1 Match': '✅' if c['h1']['match'] else '❌',
                                        'Severity': c['severity']
                                    }
                                    for c in seo_comparisons
                                ])
                                st.dataframe(df, use_container_width=True)
                    
                    st.markdown("---")
                    
                    # === EXPORT ===
                    st.markdown("## 📥 Export Reports")
                    
                    export_col1, export_col2, export_col3 = st.columns(3)
                    
                    with export_col1:
                        csv_url = f"{API_BASE_URL}/migration-projects/{project_id}/export?format=csv&section=all"
                        st.markdown(f"[📄 Download Full CSV Report]({csv_url})")
                    
                    with export_col2:
                        json_url = f"{API_BASE_URL}/migration-projects/{project_id}/export?format=json&section=all"
                        st.markdown(f"[📊 Download JSON Report]({json_url})")
                    
                    with export_col3:
                        seo_csv_url = f"{API_BASE_URL}/migration-projects/{project_id}/export?format=csv&section=seo"
                        st.markdown(f"[🎯 Download SEO Report (CSV)]({seo_csv_url})")
                
                else:
                    st.error(f"Failed to load results: {results_response['error']}")
            
            elif status['status'] == 'processing':
                st.info("⏳ Analysis in progress. This typically takes 15-25 minutes.")
                st.markdown(f"**Current stage**: {status['processingStatus']['stage'].replace('_', ' ').title()}")
                
                if st.button("🔄 Refresh Status"):
                    st.rerun()
                
                st.markdown("---")
                st.markdown("### Processing Steps:")
                st.markdown("""
                1. ✅ Parse sitemaps and data files
                2. ✅ Compare URLs
                3. ⏳ Check HTTP status codes
                4. ⏳ Validate SEO elements
                5. ⏳ Test performance
                6. ⏳ Check mobile responsiveness
                7. ⏳ Generate reports
                """)
            
            elif status['status'] == 'failed':
                st.error("❌ Processing failed. Please try creating a new project.")
            
            else:
                st.warning(f"Project status: {status['status']}")
        
        else:
            st.error(f"❌ {status_response['error']}")
            st.info("Please check your Project ID and ensure the backend is running.")

# ==========================================
# PROJECTS LIST PAGE
# ==========================================
elif page == "📋 Projects List":
    st.markdown('<p class="main-header">All Migration Projects</p>', unsafe_allow_html=True)
    
    st.info("💡 Feature coming soon: This will list all your migration projects with quick access to results.")
    
    st.markdown("""
    ### Planned Features:
    - View all projects with status
    - Quick search and filter
    - Delete old projects
    - Compare multiple projects
    - Export batch reports
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b;'>"
    "Migration Audit Platform | Built with Streamlit & Python"
    "</div>",
    unsafe_allow_html=True
)

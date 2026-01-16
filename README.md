# Migration Audit Platform - Streamlit Frontend

A beautiful, interactive dashboard for analyzing website migrations.

## Quick Start

### 1. Install Dependencies

```bash
cd streamlit-frontend
pip install -r requirements.txt
```

### 2. Configure Backend URL

Edit `.env` file:
```bash
API_URL=http://localhost:5000/api
```

Or for production:
```bash
API_URL=https://your-backend.railway.app/api
```

### 3. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Features

✨ **Beautiful UI**: Modern, responsive design with custom styling
📊 **Interactive Charts**: Plotly visualizations for all metrics
🎯 **Real-time Progress**: Track processing status in real-time
📱 **Mobile Friendly**: Works on all devices
📥 **Easy Export**: Download CSV/JSON reports
🚀 **Fast**: Optimized for performance

## Pages

### 🏠 Home
- Platform overview
- Feature highlights
- Getting started guide

### ➕ New Project
- Create migration projects
- Upload sitemaps and CSV files
- Start analysis with one click

### 📊 View Results
- Project status tracking
- Interactive visualizations:
  - URL distribution pie chart
  - Performance comparison bar charts
  - SEO score analytics
  - Mobile responsiveness metrics
- Detailed data tables
- Export options

### 📋 Projects List
- View all projects (coming soon)
- Quick access to results

## Deploying to Streamlit Cloud

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Streamlit frontend"
git push origin main
```

### 2. Deploy

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file: `app.py`
6. Click "Deploy"

### 3. Configure Secrets

In Streamlit Cloud dashboard → Settings → Secrets:

```toml
API_URL = "https://your-backend.railway.app/api"
```

**That's it!** Your app is live! 🎉

## Environment Variables

- `API_URL`: Backend API URL (required)

## Tech Stack

- **Streamlit**: Web framework
- **Plotly**: Interactive charts
- **Pandas**: Data manipulation
- **Requests**: API calls

## Customization

### Theming

Edit `.streamlit/config.toml` to customize colors:

```toml
[theme]
primaryColor="#3b82f6"
backgroundColor="#ffffff"
secondaryBackgroundColor="#f1f5f9"
textColor="#0f172a"
```

### Custom CSS

Add custom styles in `app.py`:

```python
st.markdown("""
<style>
    .your-custom-class {
        /* your styles */
    }
</style>
""", unsafe_allow_html=True)
```

## Troubleshooting

**Backend Connection Error:**
- Check `API_URL` in `.env`
- Ensure backend is running
- Check CORS settings in backend

**Charts Not Loading:**
- Update plotly: `pip install --upgrade plotly`
- Clear Streamlit cache: `streamlit cache clear`

**Slow Performance:**
- Limit data rows in tables
- Use pagination for large datasets

## Development

### File Structure

```
streamlit-frontend/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── README.md             # This file
```

### Adding New Features

1. Create new page in `app.py`
2. Add to navigation sidebar
3. Test locally
4. Deploy to Streamlit Cloud

## Support

For issues or questions:
- Check the main project documentation
- Ensure backend is properly configured
- Check browser console for errors

## License

Same as main Migration Audit Platform project.

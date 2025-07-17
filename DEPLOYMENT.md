# BENCHEXTRACT API - Cloud Deployment Guide

This guide will help you deploy the BENCHEXTRACT API to Railway and other cloud platforms.

## Prerequisites

1. **GitHub Account**: Your code should be pushed to GitHub
2. **Railway Account**: Sign up at [railway.app](https://railway.app)
3. **Environment Variables**: Prepare your environment variables

## Environment Variables Required

Create a `.env` file locally (for testing) and set these variables in Railway:

### Required Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_ANON_KEY`: Your Supabase anonymous key

### Optional Variables
- `DATABASE_URL`: PostgreSQL connection string (Railway provides this)
- `SPECS_DIRECTORY`: Path to specs directory (default: `./SPECS`)
- `MAX_ALTERNATIVE_SUPPLIERS`: Max suppliers to search (default: 5)
- `WEB_SCRAPING_TIMEOUT`: Web scraping timeout (default: 30)
- `DEBUG`: Enable debug mode (default: False)

## Deployment Steps

### 1. Push to GitHub

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit for cloud deployment"

# Add your GitHub remote
git remote add origin https://github.com/getonow/benchagentrw.git

# Push to GitHub
git push -u origin main
```

### 2. Deploy to Railway

1. **Connect GitHub Repository**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `benchagentrw` repository

2. **Configure Environment Variables**:
   - In your Railway project, go to "Variables" tab
   - Add all required environment variables listed above
   - Railway automatically provides `PORT` and `DATABASE_URL`

3. **Deploy**:
   - Railway will automatically detect the Python project
   - It will use the `Procfile` to start the service
   - The service will be available at your Railway URL

### 3. Verify Deployment

1. **Health Check**: Visit `https://your-app.railway.app/health`
2. **API Documentation**: Visit `https://your-app.railway.app/docs`
3. **Test Endpoint**: Try `https://your-app.railway.app/api/analyze-part`

## API Endpoints

Once deployed, your API will be available at:

- **Base URL**: `https://your-app.railway.app`
- **Health Check**: `GET /health`
- **API Health**: `GET /api/health`
- **Main Endpoint**: `POST /api/analyze-part`
- **File Download**: `GET /api/files/download/{filename}`
- **Available Parts**: `GET /api/parts/available`
- **Suppliers**: `GET /api/suppliers/{part_number}`

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version is specified in `runtime.txt`

2. **Environment Variables**:
   - Verify all required variables are set in Railway
   - Check variable names match exactly

3. **CORS Issues**:
   - Update CORS origins in `main.py` if needed
   - Add your frontend domain to allowed origins

4. **File Access**:
   - Ensure SPECS directory is included in the repository
   - Check file paths are relative, not absolute

### Logs

- View logs in Railway dashboard
- Use `railway logs` if using Railway CLI

## Alternative Deployment Options

### Vercel
- Create `vercel.json` configuration
- Deploy via Vercel dashboard

### Heroku
- Create `Procfile` (already done)
- Deploy via Heroku CLI or dashboard

### Docker
- Create `Dockerfile` for containerized deployment
- Deploy to any container platform

## Security Considerations

1. **Environment Variables**: Never commit `.env` files
2. **CORS**: Restrict origins in production
3. **API Keys**: Rotate keys regularly
4. **Rate Limiting**: Consider adding rate limiting for production

## Monitoring

- Railway provides basic monitoring
- Consider adding logging and monitoring tools
- Set up alerts for service health

## Support

For issues with:
- **Railway**: Check Railway documentation
- **API**: Check FastAPI documentation
- **Code**: Review logs and error messages 
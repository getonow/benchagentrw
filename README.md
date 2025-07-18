# BENCHEXTRACT - AI Negotiation & Benchmarking Agent Service

BENCHEXTRACT is an intelligent backend service that provides AI-powered supplier negotiation and benchmarking capabilities. It helps organizations identify cost-saving opportunities by comparing supplier prices, analyzing market alternatives, and generating strategic recommendations.

## Features

- **Part Analysis**: Retrieve detailed part information from database
- **Supplier Benchmarking**: Compare current suppliers against panel benchmarks
- **Web Scraping**: Find alternative suppliers on the web
- **AI-Powered Analysis**: Generate strategic recommendations using OpenAI
- **Technical Specifications**: Manage and serve technical documentation
- **RESTful API**: Easy integration with existing frontend applications

## Architecture

The service is built with FastAPI and follows a modular architecture:

```
benchagent/
├── main.py              # FastAPI application and endpoints
├── config.py            # Configuration management
├── database.py          # Database connection and session management
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic request/response models
├── data_service.py      # Database operations and business logic
├── file_service.py      # Technical specification file management
├── web_scraper.py       # Web scraping for alternative suppliers
├── ai_agent.py          # OpenAI integration and analysis
├── requirements.txt     # Python dependencies
└── SPECS/              # Technical specification files
```

## Installation

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/getonow/benchagentrw.git
   cd benchagentrw
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Copy `env_example.txt` to `.env` and configure:
   ```bash
   cp env_example.txt .env
   ```

4. **Configure the database**:
   - Set up PostgreSQL database
   - Update `DATABASE_URL` in `.env`
   - Ensure tables exist: `MASTER_FILE`, `PARTS_BENCHMARKS`, `SUPPLIER_PANEL_CATALOG`

5. **Set up OpenAI API**:
   - Get OpenAI API key from [OpenAI Platform](https://platform.openai.com/)
   - Add to `OPENAI_API_KEY` in `.env`

6. **Start the service**:
   ```bash
   python start_service.py
   ```

### Cloud Deployment

For deploying to Railway or other cloud platforms, see [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.

**Quick Railway Deployment**:
1. Push code to GitHub
2. Connect repository to Railway
3. Set environment variables in Railway dashboard
4. Deploy automatically

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:password@your-database-host:5432/benchagent` |
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4` |
| `SPECS_DIRECTORY` | Path to technical specifications | `C:/Development/benchagent/SPECS` |
| `MAX_ALTERNATIVE_SUPPLIERS` | Max web-found suppliers | `5` |
| `WEB_SCRAPING_TIMEOUT` | Web scraping timeout (seconds) | `30` |
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8000` |
| `DEBUG` | Enable debug mode | `False` |

## Database Schema

### MASTER_FILE Table
Contains part and supplier information with time-series data:

```sql
CREATE TABLE MASTER_FILE (
    suppliernumber VARCHAR(50),
    partnumber VARCHAR(50),
    suppliername VARCHAR(255),
    suppliercontactname VARCHAR(255),
    suppliercontactemail VARCHAR(255),
    suppliermanufacturinglocation VARCHAR(255),
    partname VARCHAR(255),
    material VARCHAR(255),
    material2 VARCHAR(255),
    currency VARCHAR(10),
    -- Volume columns for 2023-2025 (voljan2023, volfeb2023, etc.)
    -- Price columns for 2025 (pricejan2025, pricefeb2025, etc.)
    PRIMARY KEY (suppliernumber, partnumber)
);
```

### PARTS_BENCHMARKS Table
Contains benchmark pricing data:

```sql
CREATE TABLE PARTS_BENCHMARKS (
    partnumber VARCHAR(50) PRIMARY KEY,
    currentsuppliernumber VARCHAR(50),
    currentsuppliername VARCHAR(255),
    partname VARCHAR(255),
    currency VARCHAR(10),
    -- Supplier price columns (SUP999, SUP001, etc.)
);
```

### SUPPLIER_PANEL_CATALOG Table
Contains supplier details:

```sql
CREATE TABLE SUPPLIER_PANEL_CATALOG (
    suppliernumber VARCHAR(50) PRIMARY KEY,
    suppliername VARCHAR(255),
    suppliercontactname VARCHAR(255),
    suppliercontactemail VARCHAR(255),
    suppliermanufacturinglocation VARCHAR(255),
    website VARCHAR(255),
    description TEXT
);
```

## API Endpoints

### Main Analysis Endpoint

**POST** `/api/analyze-part`

Analyzes a part and generates comprehensive benchmark recommendations.

**Request**:
```json
{
    "part_number": "PA-10183"
}
```

**Response**:
```json
{
    "success": true,
    "message": "Successfully analyzed part PA-10183",
    "benchmark_summary": {
        "part_info": {
            "part_number": "PA-10183",
            "part_name": "Control Module Base",
            "current_price": 4.36,
            "annual_volume": 416580,
            "annual_total_spend": 1816291,
            "currency": "EUR"
        },
        "supplier_comparison": "Of the 4 benchmarked suppliers...",
        "strategic_recommendation": "Consider dual-sourcing...",
        "potential_savings": 270000,
        "savings_percentage": 15.0
    },
    "technical_spec": {
        "filename": "PA-10183 CELESTRAN.pdf",
        "file_size": 87040,
        "file_type": ".pdf",
        "download_url": "/api/files/download/PA-10183 CELESTRAN.pdf"
    },
    "suppliers": [
        {
            "supplier_number": "SUP999",
            "supplier_name": "Global Parts Ltd",
            "price": 3.71,
            "is_panel_supplier": true
        }
    ]
}
```

### Other Endpoints

- **GET** `/health` - Health check
- **GET** `/api/parts/available` - List available parts
- **GET** `/api/suppliers/{part_number}` - Get suppliers for a part
- **GET** `/api/supplier/{supplier_number}` - Get supplier details
- **GET** `/api/files/download/{filename}` - Download technical spec
- **POST** `/api/search-alternatives` - Search for web alternatives

## Usage Examples

### Python Client

```python
import requests

# Analyze a part
response = requests.post("https://your-app.railway.app/api/analyze-part", 
                        json={"part_number": "PA-10183"})
data = response.json()

print(f"Potential savings: {data['benchmark_summary']['potential_savings']} EUR")
```

### cURL

```bash
# Analyze part
curl -X POST "https://your-app.railway.app/api/analyze-part" \
     -H "Content-Type: application/json" \
     -d '{"part_number": "PA-10183"}'

# Get available parts
curl "https://your-app.railway.app/api/parts/available"
```

## Running the Service

### Development Mode

```bash
python main.py
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Workflow

1. **Input**: Part number (e.g., PA-10183)
2. **Database Query**: Retrieve part info from MASTER_FILE
3. **File Lookup**: Find technical specification in SPECS directory
4. **Benchmark Analysis**: Get supplier prices from PARTS_BENCHMARKS
5. **Web Search**: Find alternative suppliers using web scraping
6. **AI Analysis**: Generate recommendations using OpenAI
7. **Response**: Return structured JSON with analysis and recommendations

## Error Handling

The service includes comprehensive error handling:

- **404**: Part not found in database
- **500**: Internal server errors
- **Validation**: Input validation using Pydantic
- **Database**: Connection and query error handling
- **File**: Missing or corrupted file handling

## Security Considerations

- API key management through environment variables
- Input validation and sanitization
- Database connection security
- File access restrictions
- Rate limiting (recommended for production)

## Performance Optimization

- Database connection pooling
- Async file operations
- Caching for frequently accessed data
- Efficient web scraping with timeouts
- AI response caching (optional)

## Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Check `DATABASE_URL` in `.env`
   - Ensure PostgreSQL is running
   - Verify database exists

2. **OpenAI API Error**:
   - Check `OPENAI_API_KEY` in `.env`
   - Verify API key is valid
   - Check API quota

3. **File Not Found**:
   - Verify `SPECS_DIRECTORY` path
   - Check file permissions
   - Ensure files exist

4. **Web Scraping Issues**:
   - Check internet connection
   - Verify `WEB_SCRAPING_TIMEOUT` setting
   - Consider using proxy if blocked

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[Add your license information here]

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation 
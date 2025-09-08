# setup_project.py - Run this first to create the entire structure
import os
import sys

def create_project_structure():
    """Create the complete project directory structure"""
    
    directories = [
        'config',
        'src/data_collection',
        'src/data_processing', 
        'src/models',
        'src/evaluation',
        'src/visualization',
        'src/deployment',
        'data/raw',
        'data/processed',
        'data/external',
        'data/predictions',
        'databases',
        'notebooks',
        'scripts',
        'tests',
        'models_saved/lstm',
        'models_saved/arima',
        'models_saved/random_forest',
        'models_saved/prophet',
        'logs',
        'reports',
        'web_app/templates',
        'web_app/static',
        'docker'
    ]
    
    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    # Create __init__.py files
    init_files = [
        'config/__init__.py',
        'src/__init__.py',
        'src/data_collection/__init__.py',
        'src/data_processing/__init__.py',
        'src/models/__init__.py',
        'src/evaluation/__init__.py',
        'src/visualization/__init__.py',
        'src/deployment/__init__.py',
        'tests/__init__.py'
    ]
    
    for init_file in init_files:
        with open(init_file, 'w') as f:
            f.write('# This file makes Python treat the directory as a package\n')
        print(f"✓ Created: {init_file}")
    
    print("\n🎉 Project structure created successfully!")
    print("Next steps:")
    print("1. Copy the weather_collector.py to src/data_collection/")
    print("2. Create your .env file with API keys")
    print("3. Install requirements: pip install -r requirements.txt")

# ================================
# .gitignore
GITIGNORE_CONTENT = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Environment variables
.env
*.env
!.env.template

# Database
*.db
*.sqlite
*.sqlite3

# Jupyter Notebooks
.ipynb_checkpoints

# Model artifacts
models_saved/*
!models_saved/.gitkeep

# Logs
logs/*.log
*.log

# Data files (add specific ones you want to track)
data/raw/*
data/processed/*
data/external/*
data/predictions/*
!data/*/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Docker
docker-compose.override.yml

# Temporary files
*.tmp
*.temp
"""

# ================================
# README.md
README_CONTENT = """# Weather Forecasting ML Project

A comprehensive machine learning project for weather prediction using multiple algorithms and data sources.

## 🌟 Features

- **Multi-source Data Collection**: OpenWeatherMap API, NOAA, and other weather services
- **Multiple ML Models**: LSTM, ARIMA, Random Forest, and Facebook Prophet
- **Real-time Predictions**: Automated forecasting pipeline
- **Interactive Dashboard**: Web-based visualization and prediction interface
- **Comprehensive Evaluation**: Model comparison and performance metrics

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone and setup project
git clone <your-repo>
cd weather-forecasting-ml

# Create virtual environment
python -m venv weather_env
source weather_env/bin/activate  # On Windows: weather_env\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.template .env

# Edit .env with your API keys
OPENWEATHER_API_KEY=your_api_key_here
```

### 3. Initial Data Collection

```bash
# Setup project structure
python setup_project.py

# Collect initial data
python scripts/collect_initial_data.py

# Explore data
jupyter notebook notebooks/01_data_exploration.ipynb
```

## 📊 Project Structure

```
weather-forecasting-ml/
├── src/                    # Source code
├── data/                   # Data storage
├── notebooks/              # Jupyter notebooks
├── models_saved/           # Trained models
└── web_app/               # Dashboard
```

## 🔧 Usage

### Data Collection
```python
from src.data_collection.weather_collector import WeatherDataCollector
from config.config import Config

collector = WeatherDataCollector(Config.get_weather_config())
collector.collect_current_weather("New York")
```

### Model Training
```bash
python scripts/train_models.py --model lstm --city "New York"
```

### Predictions
```bash
python scripts/generate_predictions.py --days 7 --city "New York"
```

## 📈 Models Implemented

- **LSTM**: Deep learning for sequence prediction
- **ARIMA**: Statistical time series analysis
- **Random Forest**: Ensemble method for robust predictions
- **Prophet**: Facebook's forecasting tool

## 🎯 Performance Metrics

- Mean Absolute Error (MAE)
- Root Mean Square Error (RMSE)
- Mean Absolute Percentage Error (MAPE)
- R² Score

## 🌐 Web Dashboard

Launch the interactive dashboard:
```bash
cd web_app
python app.py
```

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

Your Name - your.email@example.com
Project Link: https://github.com/yourusername/weather-forecasting-ml
"""

# ================================
# requirements.txt
REQUIREMENTS_CONTENT = """# Data Collection & Processing
requests>=2.28.0
pandas>=1.5.0
numpy>=1.21.0
python-dotenv>=0.19.0
schedule>=1.2.0

# Database
sqlite3  # Built into Python
sqlalchemy>=1.4.0

# Machine Learning
scikit-learn>=1.1.0
tensorflow>=2.12.0
xgboost>=1.6.0
prophet>=1.1.0
statsmodels>=0.13.0

# Visualization
matplotlib>=3.5.0
seaborn>=0.11.0
plotly>=5.0.0

# Web Development
flask>=2.2.0
streamlit>=1.20.0
dash>=2.10.0

# Jupyter & Development
jupyter>=1.0.0
ipykernel>=6.0.0
notebook>=6.4.0

# Testing
pytest>=7.0.0
pytest-cov>=3.0.0

# Utilities
tqdm>=4.64.0
python-dateutil>=2.8.0
pytz>=2022.1

# Optional: For advanced features
# torch>=1.12.0  # Alternative to TensorFlow
# fastapi>=0.95.0  # Alternative to Flask
# uvicorn>=0.18.0  # ASGI server
"""

# ================================
# .env.template
ENV_TEMPLATE_CONTENT = """# Weather API Configuration
OPENWEATHER_API_KEY=your_openweather_api_key_here
NOAA_API_KEY=your_noaa_api_key_here

# Database Configuration
DATABASE_PATH=databases/weather_forecast.db
DATABASE_URL=sqlite:///databases/weather_forecast.db

# Data Collection Settings
CITIES=New York,London,Tokyo,Paris,Sydney,Los Angeles
COLLECTION_INTERVAL_HOURS=1
HISTORICAL_DAYS=30
API_DELAY_SECONDS=1.0

# Data Storage
EXPORT_DIR=data
RAW_DATA_DIR=data/raw
PROCESSED_DATA_DIR=data/processed

# Model Configuration
MODEL_SAVE_DIR=models_saved
PREDICTION_HORIZON_DAYS=7
TRAIN_TEST_SPLIT_RATIO=0.8

# Logging
LOG_LEVEL=INFO
LOG_DIR=logs

# Web App Configuration
FLASK_ENV=development
FLASK_DEBUG=True
WEB_APP_HOST=0.0.0.0
WEB_APP_PORT=5000

# Feature Engineering
FEATURE_ENGINEERING_ENABLED=True
SEASONALITY_FEATURES=True
LAG_FEATURES=True
ROLLING_WINDOW_SIZE=24

# Model Training
ENABLE_HYPERPARAMETER_TUNING=True
CROSS_VALIDATION_FOLDS=5
EARLY_STOPPING_PATIENCE=10

# Deployment
DEPLOYMENT_MODE=development
API_RATE_LIMIT=100
"""

def create_essential_files():
    """Create essential project files"""
    
    files_to_create = {
        '.gitignore': GITIGNORE_CONTENT,
        'README.md': README_CONTENT,
        'requirements.txt': REQUIREMENTS_CONTENT,
        '.env.template': ENV_TEMPLATE_CONTENT
    }
    
    for filename, content in files_to_create.items():
        with open(filename, 'w') as f:
            f.write(content.strip())
        print(f"✓ Created: {filename}")

if __name__ == "__main__":
    print("🏗️  Setting up Weather Forecasting ML Project...")
    print("=" * 50)
    
    create_project_structure()
    print("\n" + "=" * 50)
    create_essential_files()
    
    print("\n" + "=" * 50)
    print("🎉 Project setup complete!")
    print("\nNext steps:")
    print("1. Run: pip install -r requirements.txt")
    print("2. Copy .env.template to .env and add your API keys")
    print("3. Run: python scripts/collect_initial_data.py")
    print("4. Start exploring with: jupyter notebook")
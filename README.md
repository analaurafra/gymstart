# GymStart 🏋️

A comprehensive gym management system built with Streamlit and PostgreSQL, designed to streamline administrative operations for fitness facilities.

## Overview

GymStart is a web-based administrative panel that helps gym staff manage students (members), employees, equipment inventory, payments, and purchases efficiently. The application leverages Streamlit for rapid development and Neon PostgreSQL for reliable data management.

## Features

✨ **Core Features**:
- **Student Management**: Register and manage gym members with complete profile information
- **Employee Management**: Track staff information and employment details
- **Inventory Management**: Monitor gym equipment, quantities, and condition status
- **Payment Processing**: Record and track student payments with flexible categorization
- **Purchase Tracking**: Log all gym purchases and expenses by category
- **AI Integration**: Built-in Google Generative AI capabilities for enhanced functionality
- **Vector Search**: pgVector support for advanced similarity searches

## Tech Stack

### Backend
- **Python 3.9+**: Core programming language
- **Streamlit**: Web framework for rapid UI development
- **SQLAlchemy 2.0**: SQL toolkit and ORM
- **PostgreSQL**: Database with pgVector extension via Neon

### Database
- **Neon**: Serverless PostgreSQL platform with pgVector support
- **pgVector**: PostgreSQL extension for vector operations and AI embeddings

### Additional Technologies
- **Google Generative AI**: Integration for AI-powered features
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing

## Project Structure

```
gymstart/
├── app.py                          # Main Streamlit application
├── configurar_db.py                # Database configuration and table setup
├── pgvector_sqlalchemy_example.py  # pgVector implementation examples
├── requirements.txt                # Python dependencies
├── pages/                          # Streamlit multi-page app pages
└── README.md                       # This file
```

## Database Schema

### Tables

**funcionarios** (Employees)
- `id`: Unique identifier
- `nome`: Full name
- `cpf`: Tax ID (CPF) - Unique
- `email`: Email address - Unique
- `cargo`: Job position
- `data_contratacao`: Hire date
- `ativo`: Active status

**alunos** (Students/Members)
- `id`: Unique identifier
- `nome`: Full name
- `cpf`: Tax ID (CPF) - Unique
- `email`: Email address
- `telefone`: Phone number
- `data_cadastro`: Registration date
- `status_matricula`: Enrollment status

**inventario** (Equipment Inventory)
- `id`: Unique identifier
- `nome_equipamento`: Equipment name
- `quantidade`: Quantity available
- `data_aquisicao`: Acquisition date
- `status_conservacao`: Condition status

**pagamentos** (Payments)
- `id`: Unique identifier
- `aluno_id`: Student reference
- `valor_pago`: Amount paid
- `data_pagamento`: Payment date
- `metodo_pagamento`: Payment method
- `referencia_mes_ano`: Month/Year reference

**compras** (Purchases)
- `id`: Unique identifier
- `descricao`: Description
- `valor_total`: Total amount
- `data_compra`: Purchase date
- `categoria`: Category

## Prerequisites

Before you begin, ensure you have the following:

- Python 3.9 or higher
- A Neon PostgreSQL account (free tier available at [neon.tech](https://neon.tech))
- pip (Python package installer)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/analaurafra/gymstart.git
cd gymstart
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database Connection

**Option A: Using Secrets (Recommended for Streamlit Cloud)**

Create a file `.streamlit/secrets.toml`:

```toml
[connections.postgresql]
dialect = "postgresql"
driver = "psycopg2"
user = "neondb_owner"
password = "your_password_here"
host = "your-neon-host.neon.tech"
port = 5432
database = "neondb"
```

**Option B: Direct Configuration**

Update the `DB_URL` in `configurar_db.py`:

```python
DB_URL = "postgresql://user:password@host:5432/database?sslmode=require"
```

### 5. Initialize Database

Run the database setup script to create all necessary tables:

```bash
python configurar_db.py
```

You should see the message: `✅ Todas as tabelas foram criadas com sucesso no Neon!`

## Usage

### Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Main Features

**1. Student Registration**
   - Fill in student details (Name, CPF, Email, Phone)
   - Click "Salvar Cadastro" (Save Registration)
   - System validates CPF uniqueness automatically

**2. Access Database**
   - Use SQLAlchemy ORM or raw SQL queries
   - Example in `pgvector_sqlalchemy_example.py`

**3. Vector Search**
   - Leverage pgVector for semantic searches
   - Useful for finding similar students or recommendations

## Dependencies

Key Python packages included:

```
streamlit==1.40.0          # Web framework
sqlalchemy==2.0.30         # ORM
psycopg2-binary==2.9.9     # PostgreSQL driver
google-generativeai==0.8.6 # Google AI integration
pgvector==0.4.2            # Vector operations
pandas==2.3.3              # Data manipulation
numpy==2.4.6               # Numerical computing
```

See `requirements.txt` for the complete list.

## API Integration

### Google Generative AI

The project includes integration with Google's Generative AI. To use it:

1. Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.streamlit/secrets.toml`:

```toml
google_api_key = "your_api_key_here"
```

3. Use in your code:

```python
import google.generativeai as genai

genai.configure(api_key=st.secrets["google_api_key"])
```

## Deployment

### Streamlit Cloud

1. Push your repository to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app pointing to this repository
4. Set environment secrets in the Streamlit Cloud dashboard
5. Your app will be deployed automatically

## Security Best Practices

⚠️ **Important**: Never commit secrets to version control!

- Store database credentials in `.streamlit/secrets.toml` (add to `.gitignore`)
- Use environment variables for sensitive data
- Enable SSL mode for database connections
- Validate all user inputs before database operations
- Use parameterized queries to prevent SQL injection

## Troubleshooting

### Database Connection Issues

```
Error: "could not connect to server"
```

**Solution**: Verify your Neon connection URL and network settings. Ensure SSL mode is enabled.

### Module Not Found

```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution**: Install dependencies with `pip install -r requirements.txt`

### CPF Validation Error

The system prevents duplicate CPF entries. If you encounter this error, verify the CPF hasn't been registered previously.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please reach out to:
- GitHub: [@analaurafra](https://github.com/analaurafra)

## Roadmap

- [ ] Enhanced reporting and analytics
- [ ] Multi-user authentication system
- [ ] Payment integration (Stripe, PayPal)
- [ ] Mobile app version
- [ ] Advanced AI-powered recommendations
- [ ] Email notifications
- [ ] Data export functionality

## Acknowledgments

- [Streamlit](https://streamlit.io/) - Amazing web framework
- [Neon](https://neon.tech/) - Serverless PostgreSQL
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit
- [Google Generative AI](https://ai.google.dev/) - AI integration

---

**Happy Coding! 💪**

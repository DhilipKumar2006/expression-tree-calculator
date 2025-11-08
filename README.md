# Expression Tree Calculator

A web-based calculator that parses mathematical expressions and evaluates them using expression trees. This project demonstrates the implementation of data structures and algorithms in Python, specifically focusing on tree data structures.

## Features
- Parses mathematical expressions using expression trees
- Supports basic arithmetic operations (+, -, *, /, ^)
- Handles parentheses for grouping
- Follows standard order of operations
- Supports both numeric values and single-letter variables (e.g., a+b)
- RESTful API backend built with Flask
- Responsive frontend with clean UI
- Deployable to Render and Docker

## Project Structure
```
├── backend/
│   ├── app.py              # Flask application with expression tree logic
│   ├── requirements.txt    # Python dependencies
│   ├── render.yaml         # Render deployment configuration
│   ├── runtime.txt         # Python runtime version
│   ├── Dockerfile          # Docker configuration for backend
│   └── .dockerignore       # Files to exclude from Docker build
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── styles.css          # Styling
│   ├── script.js           # Frontend logic
│   ├── Dockerfile          # Docker configuration for frontend
│   ├── nginx.conf          # Nginx configuration
│   ├── .dockerignore       # Files to exclude from Docker build
│   └── README.md           # Frontend documentation
├── docker-compose.yml      # Docker Compose configuration
└── README.md               # This file
```

## How It Works
1. The user enters a mathematical expression in the frontend
2. The expression is sent to the backend API
3. The backend converts the infix expression to postfix notation using the Shunting Yard algorithm
4. An expression tree is built from the postfix notation
5. The tree is evaluated recursively to compute the result
6. The result is sent back to the frontend for display

## Expression Tree Algorithm
1. **Tokenization**: The input expression is broken down into tokens (numbers, variables, and operators)
2. **Infix to Postfix Conversion**: Uses the Shunting Yard algorithm to convert to postfix notation
3. **Tree Construction**: Builds a binary tree where:
   - Leaf nodes contain operands (numbers or variables)
   - Internal nodes contain operators
4. **Evaluation**: Recursively evaluates the tree from the leaves to the root

## Technologies Used
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Render (backend), GitHub Pages (frontend), Docker (local deployment)

## Setup and Installation

### Backend
1. Navigate to the backend directory:
   ```
   cd backend
   ```
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the application:
   ```
   python app.py
   ```
6. The backend will be available at `http://localhost:5000`

### Frontend
1. Start a simple HTTP server in the frontend directory:
   ```
   cd frontend
   python -m http.server 8000
   ```
2. Open your browser and go to `http://localhost:8000`
3. Make sure the backend is running
4. Enter mathematical expressions and click "Calculate"

## Docker Deployment (Local)

If you have Docker installed, you can run the entire application using Docker Compose:

1. Make sure Docker is running on your system
2. From the root directory, run:
   ```
   docker-compose up --build
   ```
3. Access the application at `http://localhost`

## Deployment

### Backend (Render)
1. Fork this repository to your GitHub account
2. Create a new Web Service on Render
3. Connect it to your forked repository
4. Set the build command to: `pip install -r requirements.txt`
5. Set the start command to: `gunicorn app:app`
6. Add an environment variable `PYTHON_VERSION` with value `3.9.15`

### Frontend (GitHub Pages)
1. Fork this repository to your GitHub account
2. Go to repository settings
3. Enable GitHub Pages from the main branch
4. The frontend will be available at `https://<your-username>.github.io/<repository-name>/`

## API Endpoints
- `GET /` - Health check endpoint
- `POST /evaluate` - Evaluate a mathematical expression
  - Request body: `{ "expression": "3 + 4 * 2" }`
  - Response: `{ "expression": "3 + 4 * 2", "result": 11, "postfix": ["3", "4", "2", "*", "+"], "infix_from_postfix": "(3 + (4 * 2))" }`

## Example Expressions
- `3 + 4 * 2` → Result: 11, Postfix: 3 4 2 * +
- `(3 + 4) * 2` → Result: 14, Postfix: 3 4 + 2 *
- `3 + 4 * 2 / (1 - 5)^2` → Result: 3.5, Postfix: 3 4 2 * 1 5 - 2 ^ / +
- `a + b * c` → Result: (a + (b * c)), Postfix: a b c * +
- `x + y / z` → Result: (x + (y / z)), Postfix: x y z / +

## Contributing
1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License
This project is open source and available under the MIT License.
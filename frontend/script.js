document.addEventListener('DOMContentLoaded', function() {
    const expressionInput = document.getElementById('expression');
    const calculateBtn = document.getElementById('calculate-btn');
    const resultDiv = document.getElementById('result');
    const postfixDiv = document.getElementById('postfix');
    
    // API endpoint - using Render backend
    const API_BASE_URL = 'https://backend-56pg.onrender.com';
    
    calculateBtn.addEventListener('click', calculateExpression);
    expressionInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            calculateExpression();
        }
    });
    
    async function calculateExpression() {
        const expression = expressionInput.value.trim();
        
        if (!expression) {
            showError('Please enter a mathematical expression');
            return;
        }
        
        try {
            showLoading();
            
            const response = await fetch(`${API_BASE_URL}/evaluate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ expression: expression })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showResult(data);
            } else {
                showError(data.error || 'An error occurred while calculating the expression');
            }
        } catch (error) {
            console.error('Error:', error);
            if (error instanceof TypeError && error.message.includes('fetch')) {
                showError('Failed to connect to the server. Please make sure the backend is running at https://backend-56pg.onrender.com');
            } else {
                showError('An error occurred: ' + error.message);
            }
        }
    }
    
    function showLoading() {
        resultDiv.innerHTML = '<div style="text-align: center;">Calculating...</div>';
        postfixDiv.innerHTML = '';
        resultDiv.className = '';
        postfixDiv.className = '';
    }
    
    function showResult(data) {
        resultDiv.innerHTML = `Result: ${data.result}`;
        postfixDiv.innerHTML = `
            <div>Postfix notation: ${data.postfix.join(' ')}</div>
            <div>Infix from postfix: ${data.infix_from_postfix}</div>
        `;
        resultDiv.className = '';
        postfixDiv.className = '';
    }
    
    function showError(message) {
        resultDiv.innerHTML = message;
        postfixDiv.innerHTML = '';
        resultDiv.className = 'error';
        postfixDiv.className = 'error';
    }
    
    // Example expressions for quick testing
    const examples = [
        '3 + 4 * 2',
        '(3 + 4) * 2',
        '3 + 4 * 2 / (1 - 5)^2',
        '2^3^2',
        '10 + 2 * 6',
        '100 * 2 + 12',
        '100 * (2 + 12)',
        '100 * (2 + 12) / 14',
        'a + b * c',
        'x + y / z'
    ];
    
    // Set a random example as placeholder
    const randomExample = examples[Math.floor(Math.random() * examples.length)];
    expressionInput.placeholder = `e.g., ${randomExample}`;
});
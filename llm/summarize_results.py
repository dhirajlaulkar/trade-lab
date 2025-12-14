import os
from groq import Groq

def generate_summary(metrics: dict, strategy_name: str, symbol: str) -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY environment variable not found. Please set it to enable AI summaries."

    client = Groq(api_key=api_key)
    
    prompt = f"""
    Analyze the following trading strategy performance and provide a brief, professional summary (max 3 sentences).
    Focus on the key metrics and whether the strategy was successful.
    
    Context:
    - Symbol: {symbol}
    - Strategy: {strategy_name}
    
    Metrics:
    - Total Return: {metrics.get('Total Return')}
    - Annualized Return: {metrics.get('Annualized Return')}
    - Sharpe Ratio: {metrics.get('Sharpe Ratio')}
    - Max Drawdown: {metrics.get('Max Drawdown')}
    - Win Rate: {metrics.get('Win Rate')}
    
    Summary:
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior quantitative analyst. Be concise."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.5,
            max_tokens=200,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"

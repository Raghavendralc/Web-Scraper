from flask import Flask, jsonify, render_template, request
import asyncio
import uuid
from datetime import datetime
from pymongo import MongoClient
from twscrape import API, gather

# Initialize Flask app
app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["trending_db"]
trends_collection = db["trends"]

# Function to fetch tweets using twscrape and save to MongoDB
async def fetch_trading_trends():
    api = API()

    # Using provided cookies for authentication
    cookies = ("ct0=3e8c4132760e670c7c93641ea7a7721e9e3f0c30f9aae10b2d63000901a07c507b3604e2e23b57b9d2b8cb7c26ced6ec9a4743d70ccd0f8267d51bf213b5e88b0dbc87b94968e981a8bfc6cc1f8b7d10;"
               " auth_token=8b6c5e88c197f5927302b16405ebdc48a5bd1a29")
    await api.pool.add_account(
        "USERNAME", "PASSWORD", "EMAIL", "PHONE", cookies=cookies
    )

    # Login all accounts
    await api.pool.login_all()

    # Clear existing data
    trends_collection.delete_many({})

    # Search for trading-related tweets
    tweets = await gather(api.search("Trending in India", limit=20))

    # Create a single document with all trends
    trends_data = []
    for i, tweet in enumerate(tweets[:20], 1):  # Limit to 20 trends
        trend = {
            "trend_number": i,
            "content": tweet.rawContent,
            "timestamp": datetime.now().isoformat()
        }
        trends_data.append(trend)

    if trends_data:
        trends_collection.insert_many(trends_data)

    return {"status": "success", "count": len(trends_data)}

# Route to trigger the script and fetch new data
@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(fetch_trading_trends())
        loop.close()
        return jsonify({"status": "success", "message": f"Successfully fetched {result['count']} trends!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Route to fetch trends with pagination
@app.route('/get_trends', methods=['GET'])
def get_trends():
    try:
        page = int(request.args.get('page', 1))
        per_page = 5  # Fixed number of trends per page

        # Calculate skip value
        skip = (page - 1) * per_page

        # Fetch trends with pagination
        trends = list(trends_collection.find({})
                     .sort("trend_number", 1)
                     .skip(skip)
                     .limit(per_page))

        # Calculate if there are more trends
        total_trends = trends_collection.count_documents({})
        has_more = (skip + per_page) < total_trends

        # Format the response
        formatted_trends = [{
            "number": trend["trend_number"],
            "content": trend["content"],
            "timestamp": trend["timestamp"]
        } for trend in trends]

        return jsonify({
            "trends": formatted_trends,
            "hasMore": has_more,
            "currentPage": page,
            "totalTrends": total_trends
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Flask route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
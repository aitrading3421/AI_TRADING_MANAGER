import psycopg2

print("=" * 50)
print("🤖 AI Trading Manager Database Setup v5")
print("=" * 50)

try:

    conn = psycopg2.connect(
        host="localhost",
        database="trading_ai",
        user="postgres",
        password="aitrading",
        port="5432"
    )

    cur = conn.cursor()

    print("✅ Connected to PostgreSQL")

except Exception as e:

    print("❌ Database Connection Failed")
    print(e)
    exit()


# ==========================================
# SYSTEM LOGS
# ==========================================

def create_system_logs():

    cur.execute("""
    CREATE TABLE IF NOT EXISTS system_logs (

        id SERIAL PRIMARY KEY,

        log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        level VARCHAR(20),

        module VARCHAR(50),

        message TEXT

    );
    """)

    print("✅ system_logs table ready")


# ==========================================
# ACCOUNT
# ==========================================

def create_account():

    cur.execute("""
    CREATE TABLE IF NOT EXISTS account (

        id SERIAL PRIMARY KEY,

        balance NUMERIC(12,2) DEFAULT 10000

    );
    """)

    cur.execute("""

    INSERT INTO account(balance)

    SELECT 10000

    WHERE NOT EXISTS (

        SELECT * FROM account

    );

    """)

    print("✅ account table ready")


# ==========================================
# PORTFOLIO
# ==========================================

def create_portfolio():

    cur.execute("""
    CREATE TABLE IF NOT EXISTS portfolio (

        id SERIAL PRIMARY KEY,

        symbol VARCHAR(20),

        shares INTEGER,

        buy_price NUMERIC(12,2),

        buy_date TIMESTAMP

    );
    """)

    print("✅ portfolio table ready")


# ==========================================
# TRADE HISTORY
# ==========================================

def create_trade_history():

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trade_history (

        id SERIAL PRIMARY KEY,

        symbol VARCHAR(20),

        action VARCHAR(10),

        shares INTEGER,

        price NUMERIC(12,2),

        total NUMERIC(12,2),

        trade_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    );
    """)

    print("✅ trade_history table ready")


# ==========================================
# MARKET DATA
# ==========================================

def create_market_data():

    cur.execute("""
    CREATE TABLE IF NOT EXISTS market_data (

        id SERIAL PRIMARY KEY,

        symbol VARCHAR(20),

        date DATE,

        close NUMERIC(12,4)

    );
    """)

    print("✅ market_data table ready")


# ==========================================
# STOCK PRICES
# ==========================================

def create_stock_prices():

    cur.execute("""
    CREATE TABLE IF NOT EXISTS stock_prices (

        id SERIAL PRIMARY KEY,

        symbol VARCHAR(20),

        trade_date DATE,

        open_price NUMERIC(12,4),

        high_price NUMERIC(12,4),

        low_price NUMERIC(12,4),

        close_price NUMERIC(12,4),

        volume BIGINT,

        UNIQUE(symbol, trade_date)

    );
    """)

    print("✅ stock_prices table ready")

# ==========================================
# AI DECISIONS
# ==========================================

def create_ai_decisions():

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ai_decisions (

        id SERIAL PRIMARY KEY,

        decision_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        ai_name VARCHAR(50),

        symbol VARCHAR(20),

        decision VARCHAR(20),

        confidence NUMERIC(5,2),

        reason TEXT

    );
    """)

    print("✅ ai_decisions table ready")


# ==========================================
# RISK LOGS
# ==========================================

def create_risk_logs():

    cur.execute("""
    CREATE TABLE IF NOT EXISTS risk_logs (

        id SERIAL PRIMARY KEY,

        log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        symbol VARCHAR(20),

        decision VARCHAR(20),

        reason TEXT

    );
    """)

    print("✅ risk_logs table ready")


# ==========================================
# NEWS CACHE
# ==========================================

def create_news_cache():

    cur.execute("""
    CREATE TABLE IF NOT EXISTS news_cache (

        id SERIAL PRIMARY KEY,

        news_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        title TEXT,

        source VARCHAR(100),

        sentiment VARCHAR(20),

        url TEXT

    );
    """)

    print("✅ news_cache table ready")


# ==========================================
# MANAGER EVENTS
# ==========================================

def create_manager_events():

    cur.execute("""
    CREATE TABLE IF NOT EXISTS manager_events (

        id SERIAL PRIMARY KEY,

        event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        event TEXT,

        status VARCHAR(30)

    );
    """)

    print("✅ manager_events table ready") 


# ==========================================
# MANAGER DECISIONS
# ==========================================

def create_manager_decisions():

    cur.execute("""
    CREATE TABLE IF NOT EXISTS manager_decisions (

    id SERIAL PRIMARY KEY,

    decision_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    symbol VARCHAR(20),

    market_decision VARCHAR(20),
    market_confidence DOUBLE PRECISION,

    news_sentiment VARCHAR(20),
    news_confidence DOUBLE PRECISION,

    risk_level VARCHAR(20),
    risk_confidence DOUBLE PRECISION,

    final_decision VARCHAR(20),

    confidence DOUBLE PRECISION,

    reason TEXT

      );
    """)

    print("✅ manager_decisions table ready")

# ==========================================
# MEMORY AI
# ==========================================

def create_memory_history():

    cur.execute("""
    CREATE TABLE IF NOT EXISTS memory_history (

        id SERIAL PRIMARY KEY,

        memory_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        symbol VARCHAR(20),

        market_decision VARCHAR(20),

        market_confidence DOUBLE PRECISION,

        news_sentiment VARCHAR(20),

        news_confidence DOUBLE PRECISION,

        risk_level VARCHAR(20),

        risk_confidence DOUBLE PRECISION,

        final_decision VARCHAR(20),

        final_confidence DOUBLE PRECISION,

        profit_loss DOUBLE PRECISION DEFAULT 0,

        outcome VARCHAR(20)

    );
    """)

    print("✅ memory_history table ready")



# ==========================================
# RUN INSTALLER
# ==========================================

create_system_logs()
create_account()
create_portfolio()
create_trade_history()
create_market_data()
create_stock_prices()
create_ai_decisions()
create_risk_logs()
create_news_cache()
create_manager_events()
create_manager_decisions()
create_memory_history()

conn.commit()

print("✅ Database setup completed successfully!")
print("=" * 50)

cur.close()
conn.close()    
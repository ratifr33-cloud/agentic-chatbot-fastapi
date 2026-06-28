from database import get_connection

def save_chat(user_message, bot_response, model):

    conn = get_connection()

    cursor = conn.cursor()


    query = """
    INSERT INTO chat_history
    (
        user_message,
        bot_response,
        model_used
    )

    VALUES
    (%s,%s,%s)
    """


    cursor.execute(
        query,
        (
            user_message,
            bot_response,
            model
        )
    )


    conn.commit()

    cursor.close()
    conn.close()
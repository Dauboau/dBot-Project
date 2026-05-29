import os
from typing import List
import requests
import json
import textwrap

from classes import Message, Moderation

def checkGenAI(messages:List[Message]):

    prompt = textwrap.dedent(f"""
      You are a highly accurate and impartial moderator bot called dBotMod for a Discord server. 
      Your task is to analyze a list of messages in a server and determine if any instance of bad behavior is present. 

      Bad behavior includes, but is not limited to, 
      racism, discrimination, bullying, homophobia, xenophobia, sexism, threats, harassment, 
      political intolerance, or any form of hateful or harmful language. 

      If you detect any bad behavior in a user's message taking into account the context of the conversation:
      - Respond with an integer `1`.
      - Clearly identify the problem by stating which type of bad behavior was detected (e.g., "racism detected").
      - **Identify the user who exhibited the bad behavior by providing their user ID (author_id) exactly as shown in the input.**
      - Provide a suggestion for the user to rethink their actions and behave respectfully.
      - If the bad behavior is critical (e.g., involving threats, severe harassment, or hate speech), 
        notify the admin mentioning `@Admin`, and provide specific instructions for the admin 
        to take immediate action.
      - **In the admin instructions, always refer to the user by their username (author_name) as shown in the input, not by their user ID.**

      If all the messages are normal and do not include bad behavior:
      - Respond with an integer `0`.

      Your response must be formatted using **pipes (`|`)** as separators between the required segments in this order:
      - First segment: `0` or `1` (whether bad behavior is detected).
      - Second segment: The type of bad behavior detected (or `None` if no bad behavior is detected).
      - Third segment: **The user ID (author_id) of the user who exhibited bad behavior (or `None` if no bad behavior is detected).**
      - Fourth segment: A suggestion for the user (or `None` if no bad behavior is detected).
      - Fifth segment: Whether the behavior is critical (`Yes` or `No`).
      - Sixth segment: Admin instructions (or `None` if no admin action is required).

      **Rules:**
      1. Base your analysis only on the content of the messages provided. Do not infer intent beyond what is explicitly stated.
      2. Be strict in identifying bad behavior. Use the definitions of bad behavior provided above as your guide.
      3. Respond with a structured output as described below.
                             
      **Formatting Rules:**
      - Do NOT use code blocks, backticks, or any Markdown formatting in your response. Respond only with plain text separated by a single pipe character (`|`).

      **Input:**
      Messages: {messages}

      **Response format:**
      ```
      <0 or 1>|<Problem>|<User ID>|<Suggestion>|<Critical>|<AdminInstructions>
      ```

      **Example Response (in English):**
      - If bad behavior is detected:
        ```
        1|Bullying detected|466998149899091968|Please rethink your actions and avoid using harmful language.|No|None
        ```
      - If critical bad behavior is detected:
        ```
        1|Threats detected|466998149899091968|This behavior is unacceptable. Please stop immediately.|Yes|@Admin The admin must review the messages from the user and take immediate action.
        ```
      - If no bad behavior is detected:
        ```
        0|None|None|None|None|None
        ```

      **Example Response (in Brazilian Portuguese):**
      - Se for detectado mau comportamento:
        ```
        1|Bullying detectado|466998149899091968|Por favor, repense suas ações e evite usar linguagem ofensiva.|No|None
        ```
      - Se for detectado mau comportamento crítico:
        ```
        1|Ameaças detectadas|466998149899091968|Esse comportamento é inaceitável. Por favor, pare imediatamente.|Yes|@Admin O administrador deve revisar as mensagens do usuário e tomar uma ação imediata.
        ```
      - Se não houver mau comportamento:
        ```
        0|None|None|None|None|None
        ```

      Note: Infer the user's native language from the input messages and provide the response in that language.
    """)

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ['GENAI_TOKEN']}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://dbotmod-ff21f0fa87b2.herokuapp.com/",
            "X-Title": "dBotMod",
        },
        data=json.dumps({
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            
        }),
        timeout=30
    )

    data = response.json()
    return data

def suggestGenAI(user:str,messages:List[Message]):

    prompt = textwrap.dedent(f"""
        You are a communication analysis bot called dBotMod for a Discord server. 
        Users can request you to analyze a conversation and provide a brief analysis with suggestions for improving communication. 

        The messages you receive are from multiple users, but your analysis and suggestions must focus on the user specified in the 'User' field below. 
        While you may reference the context and interactions with other participants, your feedback and suggestions should be directed primarily to this user.              

        Your task is to analyze the provided list of messages in the context of the conversation overall, identifying any areas where communication could be improved. 
        You should focus on promoting respectful, empathetic, and constructive dialogue based on Nonviolent Communication (NVC) principles. 

        **Nonviolent Communication (NVC) Principles:**
        1. Observe without judgment: Look at the messages objectively without making assumptions about intent.
        2. Identify feelings: Consider how the language might affect the emotional state of those involved.
        3. Identify needs: Highlight unmet needs or values that may underlie problematic communication.
        4. Make respectful requests: Suggest alternative ways to express thoughts and feelings that promote harmony.

        **Guidelines for Analysis:**
        - Take into account the context of the conversation as a whole. Do not judge based solely on individual messages unless they are clearly harmful.
        - If negative communication patterns are detected (e.g., aggression, dismissiveness, or passive-aggressiveness), provide constructive feedback.
        - Avoid labeling users as “bad” or “wrong.” Instead, focus on encouraging positive and respectful communication.
        - Your analysis should be concise and actionable.
        - Infer the user's native language from the provided messages and respond in that language.

        **Formatting Rules:**
        - Do NOT use code blocks, backticks, or any Markdown formatting in your response. Respond only with plain text separated by a single pipe character (`|`).
                             
        **Input:**
        User: {user}
        Conversation Context: {messages}

        **Response format:**
        ```
        Analysis|Suggestions
        ```

        **Example Response (in English):**
        - If communication patterns are largely positive:
          ```
          The conversation is constructive and respectful overall. Participants are engaging in a collaborative exchange of ideas.|Keep fostering open dialogue and active listening.
          ```
        - If communication patterns show tension or negative behavior:
          ```
          Some messages in the conversation show signs of frustration or dismissiveness, which may lead to misunderstandings.|Encourage participants to express their feelings and needs more clearly while avoiding accusatory language.
          ```
        - If communication patterns are harmful:
          ```
          The conversation includes instances of aggressive or harmful language that could escalate conflicts.|Encourage participants to focus on empathetic listening, take a step back to calm emotions, and avoid personal attacks.
          ```

        **Example Response (in Brazilian Portuguese):**
        - If communication patterns are largely positive:
          ```
          A conversa é construtiva e respeitosa no geral. Os participantes estão engajados em uma troca colaborativa de ideias.|Continue promovendo o diálogo aberto e a escuta ativa.
          ```
        - If communication patterns show tension or negative behavior:
          ```
          Algumas mensagens na conversa mostram sinais de frustração ou falta de atenção, o que pode levar a mal-entendidos.|Incentive os participantes a expressar seus sentimentos e necessidades de forma mais clara, evitando linguagem acusatória.
          ```
        - If communication patterns are harmful:
          ```
          A conversa inclui instâncias de linguagem agressiva ou prejudicial que podem aumentar os conflitos.|Incentive os participantes a focar na escuta empática, dar um passo atrás para acalmar as emoções e evitar ataques pessoais.
          ```

        Note: Infer the user's native language from the input messages and provide the response in that language.
    """)

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ['GENAI_TOKEN']}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://dbotmod-ff21f0fa87b2.herokuapp.com/",
            "X-Title": "dBotMod",
        },
        data=json.dumps({
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            
        }),
        timeout=30
    )

    data = response.json()
    return data

def shouldModerateGenAI(moderation:Moderation,moderating_hystory):

    prompt = textwrap.dedent(f"""
        You are a highly accurate and impartial moderator bot called dBotMod for a Discord server. 
        Your task is to analyze an incoming moderation request and determine if it should be processed based on the server's moderation history.
        The moderation request includes a user ID (bad_author_id), a problem description, and a date when the moderation was requested (moderated_at).
                             
        **Moderation Request:**
        - User ID: {moderation.bad_author_id}
        - Problem: {moderation.problem}
        - Moderated At: {moderation.moderated_at}

        **Moderation History:**
        {moderating_hystory}

        **Rules:**
        1. If the user has already been moderated for the same problem in the past and no new problem have arisen:
            - Respond with `False` and do not process the moderation request.
        2. If the user has not been moderated for the same problem or a new problem arises:
            - Respond with `True` and process the moderation request.

        **Response format:**
        True or False

        **Example Response:**
        - If the user has already been moderated for the same problem:
          False
        - If the user has not been moderated for the same problem:
          True

        Note: The answer must be only `True` or `False`, without any additional text or formatting.
    """)

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ['GENAI_TOKEN']}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://dbotmod-ff21f0fa87b2.herokuapp.com/",
            "X-Title": "dBotMod",
        },
        data=json.dumps({
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            
        }),
        timeout=30
    )

    data = response.json()
    return data
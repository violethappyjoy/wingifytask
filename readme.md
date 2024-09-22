**ReadMe for Wingify Software Pvt. Ltd. Task**
*Author: Divyanshu Bhardwaj*

# How to run the code
Step1: Steup `.env` file according to `.env.example` file and as necessary.<br>
Step2: With cwd as cloned folder, run `docker-compose up -d --build` to start the services.
Step3: Frontend will be available at `http://localhost:5173/` and API Documentation at `http://0.0.0.0:8100`(can use localhost as well).
Step4: Need to add user using `Sign Up` to test.

# My Approach
1. Workflow is divided into 3 parts: Frontend, Backend and Database.
2. Frontend is a simple `vue` template which contains a landing page and a login/signup page and upload blood report page.
3. All backend logic is done using `fast-api` and `postgresql` is used as database for users only.
4. Intution behind parsing the blood report is to extract the data and create a pipeline of crewAI agents.
5. The pipeline followed is: **Understanding Report, What is in there and organize it in terms of what requires attention**-> **Synthesize the problems in the report, what can cause harm and find material on the internet for the same**-> **Create a non-jargon mail to address the report to the end user.**
  *To get links, DuckDuckGo llm can we switched instead of Groq/LLama*
6. Lastly, the report is sent to the user via mail.
7. For security, JWT(in header) is used for authentication and password is hashed before storing in database.
8. A sample report is attached in the codebase for testing. Also, a sample mail output screenshot is attached(without links).

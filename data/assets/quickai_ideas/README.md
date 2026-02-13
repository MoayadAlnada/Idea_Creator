# QuickAI Ideas

Welcome to QuickAI Ideas – your go-to solution for breaking through the creative block. This application is designed to help bloggers, marketers, and creative professionals generate fresh content ideas effortlessly using the power of artificial intelligence. By leveraging the GPT-3 API, QuickAI Ideas can provide you with unique content suggestions that cater to your specific needs, whether you're crafting your next blog post, planning a marketing strategy, or searching for innovative project ideas.

## Prerequisites

Before you dive into the world of endless inspiration with QuickAI Ideas, ensure you have the following:

- Python (3.6 or newer)
- Node.js (LTS version recommended)
- Access to the GPT-3 API (You'll need an API key from OpenAI)
- A WordPress account for WordPress REST API integration (optional for blog management)

## Installation

1. **Clone the Project**: Start by cloning the repository to your local machine.
   
   ```bash
   git clone <repository-url>
   cd QuickAI-Ideas
   ```

2. **Setup Backend**: Install the required Python dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Frontend**: Navigate to the `frontend` directory and install the required Node.js packages.

   ```bash
   cd frontend
   npm install
   ```

4. **Environment Variables**: Set up the necessary environment variables. Create a `.env` file in the root directory of your project and define the following variables:
   
   ```plaintext
   REACT_APP_GPT3_API_KEY=<your_api_key_here>
   REACT_APP_WORDPRESS_API_URL=<your_wordpress_api_url_here>
   ```

   Ensure you replace `<your_api_key_here>` and `<your_wordpress_api_url_here>` with your actual GPT-3 API key and WordPress API URL, respectively.

## Configuration

QuickAI Ideas allows you to tailor content suggestions to suit specific industries by modifying the query parameters in the GPT-3 API requests. You can define these parameters in a configuration file or directly through the application's UI, depending on your preference.

Additionally, for CMS integration:

### WordPress:

1. Ensure you have generated API credentials (Client ID and Client Secret) from your WordPress account.
2. Add these credentials to your `.env` file for seamless operation with the WordPress REST API.

### Medium (Future Scope):

Integration with Medium is planned for future releases. This will similarly require API credentials, which should be added to the `.env` file once available.

## Running the Application

To launch QuickAI Ideas:

1. Start the backend server:

   ```bash
   python app.py
   ```

2. In a new terminal window, start the React frontend:

   ```bash
   cd frontend
   npm start
   ```

The application will now be running, and you can access it through your web browser at `http://localhost:3000`.

## Usage

1. **Generate Ideas**: Simply enter a topic or keyword into the input field on the application's homepage and click "Generate" to start receiving content ideas.
2. **Customize Results**: Use the provided filters to refine your searches based on industry, content type, and more.
3. **CMS Integration**: For WordPress users, you can directly push your new content ideas to your blog for further editing and publication, all from within the QuickAI Ideas application.

## Support

If you encounter any issues or have questions, please file an issue on the GitHub repository, and we will get back to you as soon as possible.

## Contributing

We welcome contributions to QuickAI Ideas! If you have suggestions for improvements or new features, feel free to create a pull request.

## License

QuickAI Ideas is open-source software licensed under the MIT license.
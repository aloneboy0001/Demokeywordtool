# Import libraries for HTTP requests and XML parsing
import httpx
import xml.etree.ElementTree as ET

# Main function to get keyword data from Google suggestions
async def get_keyword_data(input_keyword, input_country):
    # Get suggestions for the input keyword using Google Autocomplete
    keyword_data = await get_suggestion_keywords_google_optimized(input_keyword, input_country)

    # Prepare the result without AI analysis
    result = {
        "success": True,
        "message": "Success! Keywords Generated",
        "result": {
            "keyword_data": keyword_data,  # Returning keyword data now
        },
    }

    return result

# Function to get categorized Google suggestions for the given keyword
async def get_suggestion_keywords_google_optimized(query, countryCode):
    # Define various keyword categories for fetching suggestions
    categories = {
        "Questions": ["who", "what", "where", "when", "why", "how", "are"],
        "Prepositions": ["can", "with", "for"],
        "Alphabit": list("abcdefghijklmnopqrstuvwxyz"),
        "Comparisons": ["vs", "versus", "or"],
        "Intent-Based": ["buy", "review", "price", "best", "top", "how to", "why to"],
        "Time-Related": ["when", "schedule", "deadline", "today", "now", "latest"],
    }

    # Create a dictionary to store categorized suggestions
    categorized_suggestions = {key: {} for key in categories.keys()}

    # Iterate through each category and fetch suggestions
    for category in categories:
        for keyword in categories[category]:
            try:
                # Generate a modified query for each keyword category
                modified_query = f"{keyword} {query}"
                # Fetch suggestions asynchronously for the modified query
                category_suggestions = await get_suggestions_for_query_async(modified_query, countryCode)
                categorized_suggestions[category][keyword] = category_suggestions
            except Exception as e:
                print(f"Error in get_suggestion_keywords_google_optimized, {e}")

    # Return categorized keyword suggestions
    return categorized_suggestions

# Function to fetch suggestions from Google Autocomplete API asynchronously
async def get_suggestions_for_query_async(query, country):
    async with httpx.AsyncClient() as client:
        try:
            # Make a request to Google's Autocomplete API
            response = await client.get(f"http://google.com/complete/search?output=toolbar&gl={country}&q={query}")
            suggestions = []
            if response.status_code == 200:
                # Parse the XML response and extract suggestions
                root = ET.fromstring(response.content)
                for complete_suggestion in root.findall('CompleteSuggestion'):
                    suggestion_element = complete_suggestion.find('suggestion')
                    if suggestion_element is not None:
                        data = suggestion_element.get('data').lower()
                        suggestions.append(data)
        except Exception as e:
            print(f"Error in get_suggestions_for_query_async: {e}")
        # Return the suggestions
        return suggestions
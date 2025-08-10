from plugins.base_plugin.base_plugin import BasePlugin
from PIL import Image, ImageDraw, ImageFont
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class HackerNews(BasePlugin):
    def __init__(self, config):
        super().__init__(config)
        self.font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        self.bold_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    def fetch_hn_stories(self, num_stories=10):
        """Fetch top stories from Hacker News API"""
        try:
            # Get top story IDs
            top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            response = requests.get(top_stories_url, timeout=10)
            response.raise_for_status()
            story_ids = response.json()[:num_stories]

            stories = []
            for story_id in story_ids:
                # Fetch each story's details
                story_url = (
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                )
                story_response = requests.get(story_url, timeout=10)
                story_response.raise_for_status()
                story_data = story_response.json()

                if story_data:
                    stories.append(
                        {
                            "title": story_data.get("title", "No title"),
                            "score": story_data.get("score", 0),
                            "descendants": story_data.get(
                                "descendants", 0
                            ),  # comments count
                            "url": story_data.get("url", ""),
                            "by": story_data.get("by", "unknown"),
                        }
                    )

            return stories

        except requests.RequestException as e:
            logger.error(f"Error fetching HN stories: {e}")
            raise RuntimeError(f"Failed to fetch Hacker News stories: {e}")

    def truncate_text(self, text, max_width, draw, font):
        """Truncate text to fit within max_width pixels"""
        if draw.textbbox((0, 0), text, font=font)[2] <= max_width:
            return text

        # Binary search for the right length
        left, right = 0, len(text)
        result = ""

        while left <= right:
            mid = (left + right) // 2
            test_text = text[:mid] + "..."
            if draw.textbbox((0, 0), test_text, font=font)[2] <= max_width:
                result = test_text
                left = mid + 1
            else:
                right = mid - 1

        return result

    def generate_image(self, settings, device_config):
        """Generate the display image with HN stories"""

        # Get display dimensions
        width, height = device_config.get_resolution()

        # Handle orientation if needed
        if device_config.get_config("orientation") == "vertical":
            width, height = height, width

        # Get settings
        num_stories = int(settings.get("num_stories", 10))
        text_color = settings.get("text_color", "black")
        bg_color = settings.get("bg_color", "white")
        show_author = settings.get("show_author", "false") == "true"

        # Create image
        image = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(image)

        # Load fonts with different sizes based on display height
        if height > 600:
            title_size = 28
            header_size = 36
            meta_size = 20
        else:
            title_size = 20
            header_size = 28
            meta_size = 16

        try:
            title_font = ImageFont.truetype(self.font_path, title_size)
            header_font = ImageFont.truetype(self.bold_font_path, header_size)
            meta_font = ImageFont.truetype(self.font_path, meta_size)
        except:
            # Fallback to default font
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            meta_font = ImageFont.load_default()

        # Fetch stories
        stories = self.fetch_hn_stories(num_stories)

        # Draw header
        header_text = "Hacker News Top Stories"
        header_bbox = draw.textbbox((0, 0), header_text, font=header_font)
        header_width = header_bbox[2] - header_bbox[0]
        header_x = (width - header_width) // 2
        draw.text((header_x, 20), header_text, fill=text_color, font=header_font)

        # Draw timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        timestamp_bbox = draw.textbbox((0, 0), timestamp, font=meta_font)
        timestamp_width = timestamp_bbox[2] - timestamp_bbox[0]
        draw.text(
            (width - timestamp_width - 20, 25),
            timestamp,
            fill=text_color,
            font=meta_font,
        )

        # Draw separator line
        draw.line([(20, 70), (width - 20, 70)], fill=text_color, width=2)

        # Calculate available space for each story
        y_position = 90
        available_height = height - y_position - 20
        story_height = available_height // min(num_stories, len(stories))

        # Draw each story
        for i, story in enumerate(stories):
            if y_position + story_height > height - 20:
                break

            # Story number
            number_text = f"{i+1}."
            draw.text((20, y_position), number_text, fill=text_color, font=title_font)

            # Story title (truncated if necessary)
            title_x = 60
            max_title_width = width - title_x - 20
            truncated_title = self.truncate_text(
                story["title"], max_title_width, draw, title_font
            )
            draw.text(
                (title_x, y_position), truncated_title, fill=text_color, font=title_font
            )

            # Story metadata (points, comments, author)
            meta_y = y_position + title_size + 5
            meta_text = (
                f"↑ {story['score']} points | 💬 {story['descendants']} comments"
            )
            if show_author:
                meta_text += f" | by {story['by']}"

            draw.text((title_x, meta_y), meta_text, fill=text_color, font=meta_font)

            y_position += story_height

        return image

    def generate_settings_template(self):
        """Generate template parameters for settings page"""
        template_params = super().generate_settings_template()
        return template_params

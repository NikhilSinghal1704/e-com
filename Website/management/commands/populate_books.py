import requests, random
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from Website.models import Author, Category, Book, Tag
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the database with book and author data from the Open Library API'

    def handle(self, *args, **kwargs):
        categories = ["romance", "adventure", "comedy"]
        base_url = 'https://openlibrary.org/subjects/{category}.json?limit=20&languages=eng'
        cover_base_url = 'https://covers.openlibrary.org/b/id/{cover_id}-L.jpg'

        for category_name in categories:
            url = base_url.format(category=category_name)
            response = requests.get(url)
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"Failed to fetch data for category {category_name}"))
                continue

            data = response.json()
            books = data.get('works', [])

            for book_data in books:
                title = book_data['title']
                author_name = book_data['authors'][0]['name']
                author_first_name, author_last_name = author_name.split(' ', 1)
                author, created = Author.objects.get_or_create(first_name=author_first_name, last_name=author_last_name)

                description = book_data.get('description', '')
                if isinstance(description, dict):
                    description = description.get('value', '')
                price = random.randint(100, 1000) / 100.0  # Generate a price between $1.00 and $10.00
                
                cover_id = book_data.get('cover_id')
                cover_url = cover_base_url.format(cover_id=cover_id) if cover_id else None
                cover_content = None

                if cover_url:
                    cover_response = requests.get(cover_url)
                    if cover_response.status_code == 200:
                        cover_content = ContentFile(cover_response.content)

                # Ensure no duplicate book with the same title and author
                book, created = Book.objects.get_or_create(
                    title=title,
                    author=author,
                    defaults={
                        'price': price,
                        'description': description
                    }
                )

                if created and cover_content:
                    file_name = f"{title.replace(' ', '_')}_cover.jpg"
                    book.cover.save(file_name, cover_content, save=True)

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully added book "{title}"'))
                else:
                    self.stdout.write(self.style.WARNING(f'Book "{title}" already exists'))


                common_tags = {
                    "adventure": "Books involving exciting and risky journeys or activities.",
                    "mystery": "Books centered around solving a crime or uncovering secrets.",
                    "romance": "Books focused on love stories and romantic relationships.",
                    "fantasy": "Books featuring magical and otherworldly elements.",
                    "science fiction": "Books exploring futuristic concepts and advanced technology.",
                    "thriller": "Books filled with suspense and high-stakes situations.",
                    "horror": "Books intended to scare and unsettle the reader.",
                    "historical": "Books set in a specific historical period.",
                    "young adult": "Books aimed at teenage readers.",
                    "children": "Books written for a young audience, typically under 12.",
                    "crime": "Books revolving around criminal acts and investigations.",
                    "magic": "Books featuring magical powers and spells.",
                    "suspense": "Books that keep the reader on edge with anticipation.",
                    "biography": "Books detailing the life story of a real person.",
                    "memoir": "Books where authors narrate their own life experiences.",
                    "classic": "Books that have stood the test of time and are widely regarded as significant.",
                    "drama": "Books focusing on emotional and relational conflicts.",
                    "fiction": "Books based on imaginative narration rather than fact.",
                    "non-fiction": "Books based on factual information.",
                    "contemporary": "Books set in modern times, reflecting current issues and themes.",
                    "dystopian": "Books set in an oppressive and controlled future society.",
                    "fairy tale": "Books featuring magical and fantastical stories, often for children.",
                    "paranormal": "Books involving supernatural elements like ghosts and psychic abilities.",
                    "urban fantasy": "Books featuring magical elements in modern urban settings.",
                    "mythology": "Books based on myths and ancient stories.",
                    "supernatural": "Books involving elements beyond the natural world.",
                    "detective": "Books focused on solving crimes, typically by a detective.",
                    "espionage": "Books involving spying and undercover operations.",
                    "comedy": "Books intended to entertain and amuse the reader.",
                    "family": "Books focusing on family relationships and dynamics.",
                    "friendship": "Books centered around the bonds of friendship.",
                    "war": "Books dealing with the events and experiences of war.",
                    "survival": "Books focusing on characters' efforts to survive against odds.",
                    "time travel": "Books involving traveling through different time periods.",
                    "space": "Books set in outer space or involving space exploration.",
                    "aliens": "Books featuring extraterrestrial life forms.",
                    "vampires": "Books featuring vampire characters.",
                    "werewolves": "Books featuring werewolf characters.",
                    "ghosts": "Books featuring ghostly apparitions.",
                    "post-apocalyptic": "Books set after a catastrophic event has altered society.",
                    "epic": "Books with grand, sweeping narratives often spanning long periods.",
                    "inspirational": "Books meant to inspire and motivate readers.",
                    "gothic": "Books featuring dark, mysterious, and romantic themes.",
                    "political": "Books centered around politics and governmental issues.",
                    "psychological": "Books focusing on the psychological states of characters.",
                    "coming of age": "Books about characters growing up and maturing.",
                    "steampunk": "Books set in a world where steam power is the main source of technology.",
                    "cyberpunk": "Books set in a high-tech, futuristic society.",
                    "military": "Books focusing on military life and warfare.",
                    "religious": "Books centered around religious themes and stories.",
                    "historical fiction": "Books blending historical facts with fictional elements.",
                    "science": "Books explaining scientific concepts and discoveries.",
                    "self-help": "Books offering advice for personal improvement.",
                    "philosophy": "Books exploring fundamental questions about existence and thought.",
                    "poetry": "Books composed of poems.",
                    "art": "Books about visual arts and artists.",
                    "music": "Books about music and musicians.",
                    "travel": "Books about traveling and exploring new places.",
                    "true crime": "Books detailing real-life criminal cases.",
                    "short stories": "Books composed of short fiction stories.",
                    "anthology": "Books that are collections of works by various authors.",
                    "graphic novel": "Books told through a combination of illustrations and text.",
                    "manga": "Japanese comic books or graphic novels.",
                    "comic book": "Books featuring comic strip-style stories.",
                    "satire": "Books using humor, irony, or exaggeration to critique society.",
                    "humor": "Books meant to entertain through comedy.",
                    "legal thriller": "Books involving legal battles and courtroom drama.",
                    "medical thriller": "Books involving medical emergencies and mysteries.",
                    "western": "Books set in the American Old West.",
                    "noir": "Books with a dark, cynical style, often featuring crime.",
                    "spy thriller": "Books about espionage and spy activities.",
                    "dark fantasy": "Books with a grim, often horror-infused, fantastical setting.",
                    "high fantasy": "Books set in a completely fictional world with its own rules.",
                    "low fantasy": "Books set in the real world with some magical elements.",
                    "sword and sorcery": "Books featuring adventures with magic and combat.",
                    "portal fantasy": "Books where characters travel to a magical world through a portal.",
                    "grimdark": "Books with dark, gritty settings and morally complex characters.",
                    "alternate history": "Books exploring historical events with different outcomes.",
                    "biopunk": "Books blending biotechnology with dystopian elements.",
                    "dieselpunk": "Books set in a world where diesel power is the main source of technology.",
                    "silkpunk": "Books blending East Asian antiquity with speculative technology.",
                    "superhero": "Books featuring characters with superhuman abilities.",
                    "postmodern": "Books characterized by a departure from traditional storytelling.",
                    "literary fiction": "Books with a focus on style, character, and theme.",
                    "women's fiction": "Books focusing on women's life experiences and relationships.",
                    "magical realism": "Books blending magical elements with a realistic setting.",
                    "psychological thriller": "Books with suspenseful plots focusing on psychological manipulation.",
                    "chick lit": "Books targeting women, often with a humorous or light-hearted tone.",
                    "urban": "Books set in a contemporary urban environment.",
                    "historical romance": "Books blending romance with historical settings.",
                    "erotic romance": "Books focusing on romantic and sexual relationships.",
                    "clean romance": "Books featuring romance without explicit content.",
                    "sports": "Books centered around sports and athletes.",
                    "holiday": "Books set around specific holidays.",
                    "cozy mystery": "Books featuring light-hearted mysteries, often in small towns.",
                    "hard science fiction": "Books with a focus on scientific accuracy and technological detail.",
                    "space opera": "Books with grand, space-based adventures and epic conflict."
                }


                # Fetch and create real tags (subjects) for the book
                subjects = book_data.get('subject', [])
                for subject in subjects:
                    subject = subject.lower()
                    if subject not in common_tags.keys():
                        continue
                    category, created = Category.objects.get_or_create(
                        name=subject,
                        defaults={"description": common_tags[subject]}
                    )
                    Tag.objects.get_or_create(category=category, Book=book)


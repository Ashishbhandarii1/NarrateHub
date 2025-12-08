from main import app, db
from models import Content

sample_content = [
    {
        "title": "The Last Lighthouse Keeper",
        "category": "story",
        "language": "English",
        "tags": "motivational, adventure, solitude",
        "body": """The old lighthouse stood at the edge of the world, or so it seemed to Marcus. For forty years, he had climbed its spiral stairs each evening, lighting the beacon that guided ships through treacherous waters.

"Why don't you retire?" his daughter had asked during her last visit. "Come live in the city with us."

But Marcus knew something his daughter didn't understand. Some lights aren't meant to go out. Some guardians aren't meant to leave their posts.

Tonight, as a fierce storm raged across the sea, Marcus climbed the familiar steps once more. His knees ached, his breath came harder than it used to, but still he climbed.

At the top, he struck the match and watched the flame catch. The great lens began to turn, sending its beam across the angry waters.

Through the rain-streaked window, he saw it—a small fishing boat, caught in the storm's fury. The light found them, and slowly, they turned toward safety.

Marcus smiled. This was why he stayed. Not for the lighthouse, but for the light itself. For the hope it gave to those lost in darkness.

Some purposes are greater than comfort. Some callings outlast age. And some lights must keep burning, as long as someone is willing to tend them."""
    },
    {
        "title": "Morning Dew",
        "category": "poem",
        "language": "English",
        "tags": "nature, peaceful, morning",
        "body": """Before the world awakens,
Before the sun breaks through,
I find my quiet moment
In drops of morning dew.

Each bead a tiny mirror,
Reflecting endless sky,
A universe of wonder
In what most pass on by.

The grass bends soft beneath them,
The flowers hold them dear,
These precious gems of morning
That vanish when day's clear.

So I rise before the sunrise,
While stars still fade from view,
To find my soul's reflection
In drops of morning dew."""
    },
    {
        "title": "The Coffee Shop Confession",
        "category": "dialogue",
        "language": "English",
        "tags": "romantic, modern, heartfelt",
        "body": """"I've been coming to this coffee shop for three years," she said, stirring her latte slowly.

"I know," he replied. "I've been watching you for two of them."

She looked up, surprised. "That's either romantic or creepy."

"Probably both." He smiled nervously. "I'm the one who always orders the black coffee. The one who pretends to read the newspaper but never turns the page."

She laughed—a sound like wind chimes. "I noticed. I thought you were very dedicated to the headlines."

"I was dedicated to gathering courage." He took a deep breath. "Today I finally found it."

"And what will you do with this courage?"

"Ask you your name. Maybe buy you a coffee. Perhaps spend the rest of my life trying to make you laugh like that again."

She set down her cup. "That's quite an ambitious plan for a Tuesday morning."

"The best adventures start on ordinary days."

She smiled, extending her hand. "I'm Elena."

"I'm the luckiest man in this coffee shop, Elena. I'm David."

And just like that, between the steam of two cups and the courage of one heart, a love story began."""
    },
    {
        "title": "From Homeless to CEO: Marcus Chen's Journey",
        "category": "life",
        "language": "English",
        "tags": "inspirational, business, resilience",
        "body": """At seventeen, Marcus Chen slept under a highway overpass in Seattle. At forty-seven, he runs a tech company valued at two billion dollars. The journey between these two points is a testament to human resilience.

"I used to collect aluminum cans," Marcus recalls. "I'd walk ten miles a day, filling garbage bags. One day, I found a torn programming book in a dumpster. It changed everything."

Using library computers, Marcus taught himself to code. He wrote his first program at nineteen—a simple inventory system for a homeless shelter that had helped him.

"I didn't have money for education," he says. "But I had time and hunger—not just for food, but for knowledge. For proving that my circumstances didn't define my destiny."

His first company failed. So did his second. The third one—a cybersecurity firm—grew from a garage operation to a global enterprise.

Today, Marcus funds programs teaching coding to homeless youth. "I don't give them charity," he explains. "I give them the same thing someone gave me—an opportunity and the tools to seize it."

His advice to others facing hardship? "Your past is a story, not a prophecy. You hold the pen for every chapter that comes next."

Marcus Chen's story isn't just about success. It's about the indomitable human spirit that refuses to accept that where you start determines where you end."""
    },
    {
        "title": "The Mongol Messenger: History's First Postal System",
        "category": "history",
        "language": "English",
        "tags": "mongol empire, communication, ancient",
        "body": """Long before email, text messages, or even the telegraph, the Mongol Empire created one of history's most efficient communication networks: the Yam.

Established by Genghis Khan in the 13th century, the Yam was a sophisticated postal relay system that spanned over 50,000 kilometers across Asia and Eastern Europe. At its peak, it consisted of more than 1,400 stations, each staffed with horses, supplies, and messengers ready to ride at a moment's notice.

A messenger carrying the Khan's imperial tablet—the paiza—could demand fresh horses, food, and assistance from any station. Riders traveled up to 320 kilometers per day, far faster than any other communication method of the era.

The system was remarkably organized. Each station maintained 25 to 400 horses, depending on the route's importance. Bells attached to the riders announced their arrival, ensuring fresh mounts were ready immediately.

Marco Polo, who traveled through the empire, wrote in amazement about the Yam. He described how messages that would take months to deliver by ordinary means reached their destination in days.

The Yam's legacy extends beyond the Mongol Empire. It influenced postal systems worldwide and demonstrated that efficient communication could unite vast territories under single governance.

In our age of instant messaging, we might forget that human ingenuity has always found ways to overcome distance. The Mongol messengers, riding through steppes and mountains, were the ancient ancestors of our digital networks."""
    },
    {
        "title": "Breaking News: Community Garden Transforms Abandoned Lot",
        "category": "news",
        "language": "English",
        "tags": "community, urban renewal, environment",
        "body": """What was once an eyesore of broken concrete and weeds has become the heart of the Riverside neighborhood. The Bloom Together Community Garden celebrated its grand opening this weekend, drawing over 200 residents to witness the transformation.

"Three years ago, this lot was where people dumped garbage," says project founder Maria Santos. "Now it feeds fifty families and brings our community together."

The garden features 75 individual plots, a children's learning area, and a central gathering space with benches made from reclaimed wood. Local businesses donated supplies, and over 150 volunteers contributed more than 3,000 hours of labor.

City Councilwoman Teresa Johnson presented Santos with a community achievement award at the opening ceremony. "This garden represents everything we hope for in civic engagement," Johnson said. "It's proof that when neighbors work together, they can transform not just spaces, but lives."

The garden has already expanded beyond growing vegetables. Weekly workshops teach composting and sustainable gardening. A partnership with the local food bank ensures excess produce reaches those in need.

For longtime resident James Walker, 78, the garden means something personal. "I grew up on a farm in Alabama," he says, kneeling beside his tomato plants. "I thought I'd never feel soil between my fingers again. This place gave me that back."

The Bloom Together Garden is now accepting applications for next season's plots. Interested residents can apply at the Riverside Community Center."""
    },
    {
        "title": "The Weight of Silence",
        "category": "poem",
        "language": "English",
        "tags": "emotional, introspection, healing",
        "body": """I carried silence for so long,
It calcified inside my chest,
A stone where words belonged,
A weight that knew no rest.

The things I meant to say
Turned fossils in my throat,
Each dawn another day
Of wearing silence like a coat.

But stones, with time, will crack,
And pressure finds release,
I learned there's no way back
Except through finding peace.

So now I speak my truth,
However soft or loud,
No longer silent, still, uncouth—
I step out from the cloud.

For silence has its place,
A pause, a breath, a beat,
But never as a hiding space
From hearts that long to meet."""
    },
    {
        "title": "My Grandmother's Hands",
        "category": "life",
        "language": "English",
        "tags": "family, memories, heritage",
        "body": """I remember my grandmother's hands. They were maps of a life fully lived—each wrinkle a road traveled, each age spot a sunset witnessed.

Those hands kneaded bread every Sunday morning. They patched clothes, planted gardens, and wiped away tears. They held books open for bedtime stories and clasped in prayer before meals.

"Your hands will tell your story someday," she used to say, pressing my small fingers between her weathered palms. "Make sure it's a story worth telling."

She came to America at nineteen with nothing but those hands and a determination to build something lasting. She worked in factories, cleaned houses, saved every penny. Those hands put two children through college and built a home from nothing.

When Alzheimer's took her memories, her hands remembered. She would still knead invisible dough, still reach out to comfort. The body holds what the mind releases.

I look at my own hands now—softer than hers ever were, unfamiliar with her hardships. But I see her in them. In the way I shape bread dough. In the gesture I make when reaching for someone in pain.

She passed three years ago, but her hands live on. In mine. In my daughter's. In every loaf of bread, every garden planted, every hand extended in love.

That, I think, is her true legacy. Not possessions, not wealth, but the continuation of a touch that heals, creates, and loves.

Grandma, wherever you are—these hands remember."""
    }
]

def seed_database():
    with app.app_context():
        existing = Content.query.count()
        if existing > 0:
            print(f"Database already has {existing} content items. Skipping seed.")
            return
        
        for item in sample_content:
            content = Content(
                title=item["title"],
                category=item["category"],
                language=item["language"],
                tags=item["tags"],
                body=item["body"]
            )
            db.session.add(content)
        
        db.session.commit()
        print(f"Successfully seeded {len(sample_content)} content items.")

if __name__ == "__main__":
    seed_database()

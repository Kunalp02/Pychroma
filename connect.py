# # Import the necessary modules
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from chromadb.utils import embedding_functions

# Create a Chroma client by specifying the host and port where the Chroma server is running
client = chromadb.HttpClient(host="localhost", port=8000)


class MyEmbeddingFunction(EmbeddingFunction[Documents]):
    def __call__(self, input: Documents) -> Embeddings:
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="BAAI/bge-large-en-v1.5")
        embeddings = sentence_transformer_ef(input)
        return embeddings


custom = MyEmbeddingFunction()

documents = [
    "The latest iPhone model comes with impressive features and a powerful camera.",
    "Exploring the beautiful beaches and vibrant culture of Bali is a dream for many travelers.",
    "Einstein's theory of relativity revolutionized our understanding of space and time.",
    "Traditional Italian pizza is famous for its thin crust, fresh ingredients, and wood-fired ovens.",
    "The American Revolution had a profound impact on the birth of the United States as a nation.",
    "Regular exercise and a balanced diet are essential for maintaining good physical health.",
    "Leonardo da Vinci's Mona Lisa is considered one of the most iconic paintings in art history.",
    "Climate change poses a significant threat to the planet's ecosystems and biodiversity.",
    "Startup companies often face challenges in securing funding and scaling their operations.",
    "Beethoven's Symphony No. 9 is celebrated for its powerful choral finale, 'Ode to Joy.'",
    "The exploration of deep space holds the promise of uncovering new celestial phenomena and expanding our cosmic understanding.",
    "The intricate dance of quantum particles challenges our traditional notions of reality and opens doors to revolutionary technological advancements.",
    "Ancient civilizations, such as the Egyptians and Mesopotamians, laid the foundations for modern architecture and urban planning.",
    "Environmental conservation efforts play a crucial role in preserving endangered species and maintaining ecological balance.",
    "The study of artificial intelligence continues to push the boundaries of what machines can achieve, raising ethical considerations along the way.",
    "The human genome project marked a milestone in genetic research, unraveling the complexities of our DNA and unlocking medical possibilities.",
    "Contemporary literature reflects the diverse voices and perspectives of our global society, fostering empathy and cultural understanding.",
    "The intricate world of cryptography is essential in safeguarding sensitive information and ensuring secure digital communication.",
    "Advancements in renewable energy technologies hold the key to mitigating the impact of climate change and transitioning to a sustainable future.",
    "The art of storytelling, passed down through generations, remains a powerful means of preserving cultural heritage and fostering connections.",
    "The study of neuroplasticity reveals the brain's remarkable ability to adapt and reorganize, providing hope for innovative approaches to mental health.",
    "Space exploration missions, such as Mars rovers, expand our knowledge of the cosmos and lay the groundwork for potential interplanetary travel.",
    "Understanding the principles of quantum computing may revolutionize the field of information processing, unlocking new frontiers in computational power.",
    "Philanthropic initiatives play a crucial role in addressing global challenges, promoting social justice, and fostering community development.",
    "The fusion of technology and healthcare has the potential to revolutionize patient care, from personalized medicine to remote diagnostic \
    The fusion of technology and healthcare has the potential to revolutionize patient care, from personalized medicine to remote diagnostics\
    The fusion of technology and healthcare has the potential to revolutionize patient care, from personalized medicine to remote diagnostics\
    The fusion of technology and healthcare has the potential to revolutionize patient care, from personalized medicine to remote diagnostics\
    The fusion of technology and healthcare has the potential to revolutionize patient care, from personalized medicine to remote diagnostics\
    The fusion of technology and healthcare has the potential to revolutionize patient care, from personalized medicine to remote diagnostics\
    The fusion of technology and healthcare has the potential to revolutionize patient care, from personalized medicine to remote diagnostics\
    The fusion of technology and healthcare has the potential to revolutionize patient care, from personalized medicine to remote diagnostics\
    The fusion of technology and healthcare has the potential to revolutionize patient care, from personalized medicine to remote diagnostics\
    The fusion of technology and healthcare has the potential to revolutionize patient care, from personalized medicine to remote diagnostics\
    The fusion of technology and healthcare has the potential to revolutionize patient care, from personalized medicine to remote diagnostics"
]

metadatas = [
    {"source": "web", "novel": "xyz"},
    {"source": "novel"},
    {"source": "web"},
    {"source": "web", "novel": "xyz"},
    {"source": "web"},
    {"source": "novel"},
    {"source": "web"},
    {"source": "novel"},
    {"source": "web"},
    {"source": "novel"},
    {"source": "web"},
    {"source": "novel"},
    {"source": "web"},
    {"source": "novel"},
    {"source": "tech"},
    {"source": "web"},
    {"source": "novel"},
    {"source": "web"},
    {"source": "novel"},
    {"source": "tech"},
    {"source": "web"},
    {"source": "novel"},
    {"source": "web"},
    {"source": "novel"},
    {"source": "tech"},
]



collection = client.get_collection(name="testlocal", embedding_function=custom)
result = collection.get(
    include=["embeddings", "documents", "metadatas"]
)

query = "iphone"
metadata_filters = {
    "source": "web",
    "novel": "xyz",
}

where_clause = {
    "$and": [
        {key: {"$eq": value}} for key, value in metadata_filters.items()
    ]
}

result = collection.query(
    query_texts=query,
    n_results=8,
    where=where_clause,
)

for key, value in result.items():
    print(f"{key} {value}")



# cltn = client.get_or_create_collection(name="testlocal", embedding_function=custom)

# cltn.add(
#     ids= [f"id{i}" for i in range(1, len(documents)+1)] ,
#     documents=documents,
#     metadatas=metadatas,
# )

# result = collection.query(
#     query_texts="iphone",
#     n_results=2,
#     where=[{"source":"web", "source":"xyz"}]
# )

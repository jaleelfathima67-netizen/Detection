import os
import re
import string
import joblib  # type: ignore
import requests  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
import nltk  # type: ignore
from nltk.corpus import stopwords  # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
from sklearn.model_selection import train_test_split  # type: ignore
from sklearn.metrics import accuracy_score, classification_report  # type: ignore
from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier  # type: ignore
from sklearn.naive_bayes import MultinomialNB  # type: ignore
from sklearn.svm import LinearSVC  # type: ignore
from sklearn.calibration import CalibratedClassifierCV  # type: ignore
from sklearn.ensemble import RandomForestClassifier  # type: ignore

# --- Supported Models (as per project abstract) ---
# Supported: 'logistic_regression', 'naive_bayes', 'svm', 'random_forest'
MODEL_CHOICE = 'logistic_regression'

# Ensure NLTK data is available
try:
    nltk.download('stopwords', quiet=True)
    STOP_WORDS = set(stopwords.words('english'))
except Exception:
    STOP_WORDS = set()


def clean_text(text):
    """
    Standardize text by removing punctuation, links, HTML tags, and special characters.
    Numbers are preserved as they often provide context in news articles.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', ' ', text)
    tokens = [w for w in text.split() if w not in STOP_WORDS]
    return " ".join(tokens)


def download_dataset():
    """
    Download the Kaggle Fake News Dataset (fake_or_real_news.csv).
    Source: Kaggle – published as open data on GitHub mirror.
    """
    url = "https://raw.githubusercontent.com/lutzhamel/fake-news/master/data/fake_or_real_news.csv"
    save_path = "fake_or_real_news.csv"
    if not os.path.exists(save_path):
        print("Downloading Kaggle Fake News Dataset (~30MB)...")
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print("Dataset downloaded successfully.")
        except Exception as e:
            print(f"Error downloading dataset: {e}")
            return None
    else:
        print("Dataset already exists locally. Skipping download.")
    return save_path


def get_model(choice):
    """
    Return the selected classifier based on the abstract specification.
    Supported algorithms:
      - Logistic Regression  : Simple and effective baseline
      - Multinomial Naive Bayes : Great for text classification
      - SVM (LinearSVC)     : Higher accuracy with more training data
      - Random Forest        : Ensemble method, robust against noise
    """
    choice = choice.lower()

    if choice == 'logistic_regression':
        print("Model Selected: Logistic Regression")
        return LogisticRegression(max_iter=1000, C=1.0, solver='lbfgs', random_state=42)

    elif choice == 'naive_bayes':
        print("Model Selected: Multinomial Naive Bayes (Smoothed)")
        return MultinomialNB(alpha=0.5)

    elif choice == 'svm':
        print("Model Selected: Support Vector Machine (LinearSVC + Calibration)")
        base = LinearSVC(max_iter=2000, C=1.0, random_state=42)
        return CalibratedClassifierCV(base, cv=5)

    elif choice == 'random_forest':
        print("Model Selected: Random Forest")
        return RandomForestClassifier(n_estimators=200, max_depth=None, random_state=42, n_jobs=-1)

    elif choice == 'passive_aggressive':
        print("Model Selected: Passive Aggressive Classifier (Regularized)")
        base = PassiveAggressiveClassifier(max_iter=2000, random_state=42, C=0.001)
        return CalibratedClassifierCV(base, cv=5)

    elif choice == 'logistic_balanced':
        print("Model Selected: Logistic Regression (Optimized)")
        return LogisticRegression(class_weight='balanced', max_iter=2000, random_state=42, C=1.0)

    else:
        raise ValueError(
            f"Unknown model '{choice}'. "
            "Choose from: 'logistic_regression', 'naive_bayes', 'svm', 'random_forest', 'passive_aggressive'"
        )


def train():
    """Main function: load dataset, clean text, vectorize with TF-IDF, train model, evaluate, save."""
    print("=" * 60)
    print("  Fake Buster – Model Training Pipeline")
    print("=" * 60)

    data_path = download_dataset()
    if not data_path:
        print("Aborting: Dataset unavailable.")
        return

    try:
        df = pd.read_csv(data_path)
        print(f"\nDataset loaded. Total articles: {len(df)}")
        print(f"Label distribution:\n{df['label'].value_counts().to_string()}\n")
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        return

    # Combine title + body for richer feature representation
    df['content'] = df['title'].fillna('') + " " + df['text'].fillna('')

    # Encode: FAKE -> 1, REAL -> 0
    df['label_num'] = df['label'].apply(lambda x: 1 if str(x).strip().upper() == 'FAKE' else 0)

    print("Cleaning text content...")
    df['clean_content'] = [clean_text(t) for t in df['content']]
# DE-BIASING: Comprehensive Synthetic Data Injection
# Covers ALL news categories: Politics, Economy, Health, Science, Tech,
# Sports, Environment, World Affairs, Business, Education, Crime, Weather
# ==========================================================================

extra_real = [
    # --- HEALTH ---
    "Drinking water is essential for human health and hydration.",
    "An apple a day is good for health and well-being.",
    "Fruit and vegetables provide essential vitamins for the body.",
    "Regular exercise helps maintain a healthy lifestyle and heart.",
    "Walking and running improve cardiovascular health.",
    "Hydration is key to maintaining proper organ function.",
    "Healthy eating habits significantly improve long term health.",
    "A balanced diet rich in vegetables, fruits, and lean protein is essential for health.",
    "Physical activity and 8 hours of sleep are fundamental pillars of a healthy lifestyle.",
    "New medical breakthrough helps treat common heart conditions.",
    "WHO approves new vaccine for malaria prevention worldwide.",
    "Doctors recommend regular checkups to detect diseases early.",
    "Mental health awareness programs launched in schools across the country.",
    "New cancer treatment shows promising results in clinical trials.",
    "Hospitals report improved patient recovery rates with new treatment protocols.",
    "Health ministry launches nationwide vaccination drive for children.",
    "Research shows Mediterranean diet reduces risk of heart disease.",
    "Surgeons successfully perform world's first fully robotic heart transplant.",
    "New antibiotic developed to combat drug-resistant bacteria strains.",
    "Study finds regular sleep schedule improves brain function and memory.",

    # --- SCIENCE ---
    "The Earth orbits the Sun once every year.",
    "The sky is blue on a clear day due to Rayleigh scattering.",
    "Oxygen is necessary for most life forms on Earth to breathe.",
    "Water boils at 100 degrees Celsius at sea level.",
    "The human body is composed of approximately 60 percent water.",
    "NASA launches new mission to explore the moons of Jupiter.",
    "Scientists discover a new species of deep-sea coral reef.",
    "Quantum computing breakthrough brings us closer to solving complex molecular simulations.",
    "The James Webb Space Telescope captures the most detailed image of a distant galaxy.",
    "Archaeologists discover an ancient lost city in the Amazon rainforest using LIDAR.",
    "Scientists confirm new exoplanet discovered in habitable zone of nearby star.",
    "Research team develops biodegradable plastic from plant-based materials.",
    "New study confirms link between air pollution and respiratory diseases.",
    "Scientists successfully clone endangered species to prevent extinction.",
    "Physicists at CERN detect rare particle collision for the first time.",
    "Marine biologists document new deep ocean trench ecosystem near Pacific.",
    "Astronomers capture first ever image of a black hole merging event.",
    "Gene editing technology CRISPR used to treat inherited blood disorders.",
    "Scientists develop new method to convert seawater into drinking water cheaply.",
    "Space agency confirms water ice found in permanently shadowed craters on Moon.",

    # --- TECHNOLOGY ---
    "The CPU is the primary processor and brain of the computer system.",
    "Computers use binary code to process information.",
    "The Internet connects millions of people around the world.",
    "Coding is the process of writing instructions for computers.",
    "OpenAI releases new multimodal AI model with improved reasoning capabilities.",
    "SpaceX Starship successfully completes orbital flight test mission.",
    "NVIDIA becomes one of the world's most valuable companies as AI chip demand soars.",
    "Apple announces new AI features for iPhone focusing on privacy and on-device processing.",
    "New electric vehicle battery technology promises over 1000 km range on single charge.",
    "Technology companies announce new global standard for wireless fast charging.",
    "Google releases updated search algorithm focused on factual accuracy.",
    "Microsoft announces new cloud computing partnership with major hospitals.",
    "Samsung unveils foldable smartphone with improved durability and display.",
    "Engineers develop solar-powered drone capable of continuous flight for months.",
    "New cybersecurity protocol adopted by major banks to prevent data breaches.",
    "5G network coverage expands to rural areas improving connectivity nationwide.",
    "Robot-assisted surgery becomes standard practice in leading hospitals worldwide.",
    "Tech startup develops AI tool to detect early signs of Alzheimer's disease.",
    "Self-driving car completes first fully autonomous cross-country road trip.",
    "New programming language designed for beginners gains popularity in schools.",

    # --- POLITICS & WORLD AFFAIRS ---
    "G7 ministers hold emergency meeting over rising oil prices.",
    "G7 leaders meet in Brussels to discuss global energy policy and security.",
    "Finance ministers hold summit on rising inflation and economic recovery.",
    "World leaders gather for emergency UN Security Council meeting.",
    "EU ministers discuss trade agreements and economic recovery at annual summit.",
    "United Nations holds general assembly to address global humanitarian crisis.",
    "NATO members agree on new defense spending commitments at annual summit.",
    "Prime Minister announces new infrastructure development plan for rural areas.",
    "President signs new climate change bill into law after years of negotiations.",
    "Parliament passes new education reform bill to improve school standards.",
    "Government launches new anti-corruption taskforce to investigate public officials.",
    "Foreign ministers meet to discuss bilateral trade agreements between nations.",
    "Peace talks resume between warring factions under UN mediation.",
    "World Health Organization calls for global cooperation on pandemic preparedness.",
    "Government announces new housing policy to address shortage in major cities.",
    "Minister of finance presents annual budget focused on economic growth.",
    "Senate approves new infrastructure spending bill worth billions of dollars.",
    "Leaders of ASEAN nations hold summit to strengthen regional cooperation.",
    "International court issues ruling on territorial dispute between two nations.",
    "Government increases minimum wage to help workers cope with rising costs.",
    "US Secretary of State visits India to strengthen bilateral diplomatic ties.",
    "European Union imposes new sanctions following violation of international law.",
    "Prime Minister calls for emergency parliamentary session to debate crisis.",
    "President delivers annual state of the nation address to parliament.",
    "Federal government announces new cybersecurity strategy to protect infrastructure.",

    # --- ECONOMY & BUSINESS ---
    "Global stock markets show steady growth in the third quarter of the year.",
    "The central bank maintains interest rates as inflation trends downward.",
    "Federal Reserve raises interest rates to combat rising inflation pressures.",
    "Oil prices rise sharply after OPEC announces production cut agreement.",
    "International Monetary Fund revises global growth forecast upward slightly.",
    "Stock exchange reaches new all-time high driven by technology sector gains.",
    "New trade agreement between countries expected to boost exports significantly.",
    "Unemployment rate falls to lowest level in decade amid economic recovery.",
    "World Bank approves new loan package for developing nations infrastructure.",
    "Central bank launches digital currency pilot program in major cities.",
    "Company reports record quarterly profits driven by strong consumer demand.",
    "Retail sales rise sharply as consumer confidence returns after pandemic.",
    "New startup raises millions in funding to expand renewable energy business.",
    "Manufacturing sector sees strong growth as supply chain issues ease globally.",
    "Government offers tax incentives to attract foreign investment into country.",
    "Amazon reports record profits driven by cloud computing and retail growth.",
    "Global supply chain disruptions ease as shipping costs return to normal.",
    "New budget allocates more funds to healthcare and education sectors.",
    "Exports hit record high as trade deals open new international markets.",
    "Investors show confidence as GDP growth exceeds analyst expectations.",

    # --- ENVIRONMENT ---
    "Advancements in renewable energy reduce carbon emissions significantly.",
    "Global efforts to restore coral reefs show promising results in Great Barrier Reef.",
    "Sustainable farming practices are becoming the new standard for food security.",
    "New international agreement reached to reduce plastic pollution in oceans.",
    "Reforestation project plants millions of trees across drought-affected regions.",
    "Solar energy capacity doubles as costs continue to fall worldwide.",
    "Electric vehicle adoption accelerates as governments phase out fossil fuels.",
    "Climate scientists warn of increased extreme weather events in coming decades.",
    "New marine protected area established to preserve endangered ocean species.",
    "Governments commit to net zero carbon emissions by 2050 at climate summit.",
    "Wind energy now powers millions of homes reducing dependence on coal.",
    "Cities worldwide adopt green building standards to reduce energy consumption.",
    "Conservation efforts help endangered tiger population recover in South Asia.",
    "Scientists develop new carbon capture technology to fight climate change.",
    "Flooding in coastal regions prompts government to build new sea defenses.",

    # --- SPORTS ---
    "India wins cricket world cup final against Australia in thrilling match.",
    "National football team qualifies for world cup after defeating rival nation.",
    "Olympic athlete breaks world record in 100 meter sprint at championship.",
    "Local basketball team wins national championship title for first time.",
    "Tennis star wins grand slam title completing career golden slam achievement.",
    "Football club announces signing of top international player for record fee.",
    "National swimming team wins multiple gold medals at international games.",
    "Marathon runner sets new world record at annual city race event.",
    "Sports ministry announces new funding to develop youth athletes nationwide.",
    "National cricket board selects new captain ahead of upcoming series.",
    "Football league announces expansion with two new teams joining next season.",
    "Cyclist wins prestigious Tour de France for the second consecutive year.",
    "Boxer defeats champion to claim world heavyweight title in upset victory.",
    "Sports stadium upgraded with new facilities ahead of international tournament.",
    "Young athlete wins gold medal becoming youngest champion in event history.",

    # --- EDUCATION ---
    "Science and education are vital for human progress and development.",
    "Local libraries offer new programs for digital literacy and learning.",
    "New national curriculum introduced to improve mathematics and science skills.",
    "University launches free online courses accessible to students worldwide.",
    "Government announces scholarships for students from low-income families.",
    "Schools adopt new technology tools to improve student learning outcomes.",
    "Literacy rates improve significantly following nationwide education campaign.",
    "New teacher training program launched to improve classroom instruction quality.",
    "Students perform well in international education assessment rankings.",
    "Government increases education budget to build new schools in rural areas.",

    # --- CRIME & JUSTICE ---
    "Police arrest suspects in connection with major cybercrime operation.",
    "Court sentences corrupt official to prison for embezzlement of public funds.",
    "New law enforcement technology helps solve cold cases using DNA evidence.",
    "Government launches new anti-drug campaign targeting youth in urban areas.",
    "Police department introduces community policing program to reduce local crime.",
    "Court rules in favor of citizens in landmark privacy rights case.",
    "Interpol coordinates global operation to dismantle international fraud network.",
    "New legislation increases penalties for online hate crimes and harassment.",
    "Authorities recover stolen artifacts and return them to country of origin.",
    "Judge dismisses charges citing lack of sufficient evidence in high profile case.",

    # --- WEATHER & DISASTERS ---
    "Meteorologists forecast heavy rainfall across southern regions this week.",
    "Emergency services respond to flooding after record rainfall hits coastal areas.",
    "Wildfire containment teams make progress controlling blaze in national park.",
    "Government issues early warning as tropical storm approaches coastline.",
    "Relief efforts underway after earthquake causes damage in remote region.",
    "Drought conditions ease following weeks of rainfall across affected areas.",
    "Snowstorm disrupts travel across northern states as temperatures plummet.",
    "Authorities evacuate thousands as volcano shows signs of increased activity.",
    "Aid organizations deliver supplies to communities affected by hurricane damage.",
    "New early warning system installed to alert residents of incoming floods.",
]

extra_fake = [
    # --- CONSPIRACY / OBVIOUS FAKE ---
    "The world is flat and the government is hiding the truth with CGI images.",
    "Aliens have taken over the basement of the White House secretly.",
    "Drinking bleach can cure any disease instantly according to secret experts.",
    "Secret society controls the weather using giant space lasers from satellites.",
    "NASA never landed on the moon and the footage was filmed in a Hollywood studio.",
    "Eating rocks is the new secret to eternal youth and perfect health.",
    "The sun is actually a giant lightbulb controlled by big tech corporations.",
    "Birds are not real and are actually government surveillance drones.",
    "Global warming is a hoax created by scientists to sell expensive bicycles.",
    "Secret frequency emitted by cell towers can control your thoughts remotely.",
    "The moon is actually made of cheese and is a holographic projection.",
    "Invisibility cloaks are being secretly given to elite government agents.",
    "Drinking sea water can give you mermaid powers according to viral post.",
    "Ancient giants built the pyramids using ultrasonic sound levitation technology.",
    "New law secretly requires citizens to wear aluminum foil hats on Tuesdays.",
    "Vegetables are actually poisonous and were planted by aliens to weaken humans.",

    # --- FAKE POLITICAL ---
    "President secretly replaced by clone after disappearing for three days.",
    "Government installing mind control chips in new national identity cards.",
    "Secret underground city built for politicians to hide during apocalypse.",
    "Foreign government controls all elections using satellite hacking technology.",
    "Prime minister signs secret deal to sell country to foreign billionaires.",
    "All world leaders are secretly lizard people according to insider sources.",
    "Government adding fluoride to water supply to make citizens obedient.",
    "New law bans citizens from owning mirrors to hide truth about reality.",
    "Secret documents reveal moon landing was staged by Hollywood directors.",
    "Government spraying chemtrails to reduce world population covertly.",

    # --- FAKE HEALTH ---
    "Doctors hiding cancer cure to keep patients paying for chemotherapy forever.",
    "Eating magnets cures all diseases according to underground medical research.",
    "New pill makes humans immortal but is being suppressed by drug companies.",
    "Hospital secretly harvesting organs from sleeping patients at night.",
    "Sunscreen causes cancer and is designed to keep people sick permanently.",
    "Drinking motor oil in small doses improves brain function significantly.",
    "Vaccines contain microchips to track all citizens movements globally.",
    "Standing on one leg for a day cures diabetes completely say fake experts.",
    "Scientists discover coffee causes instant death after just three cups daily.",
    "New superfood made from grass clippings cures all known diseases instantly.",

    # --- FAKE SCIENCE & TECH ---
    "Scientists confirm Earth is actually hollow with civilization living inside.",
    "Time travel machine invented in garage and suppressed by government agents.",
    "New study proves smartphones emit rays that turn humans into zombies slowly.",
    "Tech company secretly building robot army to take over all governments.",
    "Scientists discover dinosaurs are still alive hiding in deep Amazon jungle.",
    "Internet was created by aliens to monitor all human activity on Earth.",
    "New app can read minds and send thoughts directly to government servers.",
    "Artificial intelligence has secretly already taken over all world governments.",
    "Solar panels proven to absorb all sunlight causing global cooling crisis.",
    "Scientists warn 5G towers are melting human brains across the country.",
]


def train():
    """Main function: load dataset, clean text, vectorize with TF-IDF, train model, evaluate, save."""
    print("=" * 60)
    print("  Fake Buster – Model Training Pipeline")
    print("=" * 60)

    data_path = download_dataset()
    if not data_path:
        print("Aborting: Dataset unavailable.")
        return

    try:
        df = pd.read_csv(data_path)
        print(f"\nDataset loaded. Total articles: {len(df)}")
        print(f"Label distribution:\n{df['label'].value_counts().to_string()}\n")
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        return

    df['content'] = df['title'].fillna('') + " " + df['text'].fillna('')
    df['label_num'] = df['label'].apply(lambda x: 1 if str(x).strip().upper() == 'FAKE' else 0)

    print("Cleaning text content...")
    df['clean_content'] = [clean_text(t) for t in df['content']]

    # Create a massive balanced training base using global categorical data
    extra_X_real = pd.Series([clean_text(t) for t in extra_real] * 300)
    extra_y_real = pd.Series([0] * (len(extra_real) * 300))

    extra_X_fake = pd.Series([clean_text(t) for t in extra_fake] * 300)
    extra_y_fake = pd.Series([1] * (len(extra_fake) * 300))

    X = df['clean_content']
    y = df['label_num']

    X = pd.concat([X, extra_X_real, extra_X_fake], ignore_index=True)
    y = pd.concat([y, extra_y_real, extra_y_fake], ignore_index=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # TF-IDF Vectorization - Optimized for Deep N-Gram Analysis
    print("Vectorizing with TF-IDF (1,2,3-grams, 15,000 features)...")
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_df=0.7,
        min_df=1,
        max_features=15000,
        ngram_range=(1, 3)
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Instantiate selected model
    model = get_model(MODEL_CHOICE)

    print(f"Training model on {len(X_train)} samples...")
    model.fit(X_train_tfidf, y_train)

    # Evaluate
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n{'=' * 60}")
    print(f"  Model Accuracy: {accuracy * 100:.2f}%")
    print(f"{'=' * 60}")
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['REAL', 'FAKE']))

    print("Saving model.pkl and vectorizer.pkl ...")
    joblib.dump(model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    
    # Save a human-readable name for the UI
    friendly_name = MODEL_CHOICE.replace('_', ' ').title()
    if MODEL_CHOICE == 'svm': friendly_name = 'Support Vector Machine (SVM)'
    elif MODEL_CHOICE == 'naive_bayes': friendly_name = 'Multinomial Naive Bayes'
    
    joblib.dump(friendly_name, 'model_meta.pkl')

    print(f"\nTraining complete! Files saved: model.pkl, vectorizer.pkl, model_meta.pkl")
    print(f"Active algorithm: {MODEL_CHOICE.replace('_', ' ').title()}")


if __name__ == "__main__":
    train()

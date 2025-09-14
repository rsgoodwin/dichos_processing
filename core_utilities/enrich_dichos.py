#!/usr/bin/env python3
"""
Comprehensive Dicho Enrichment with LLM Analysis
Adds detailed metadata matching the existing database format
Incorporates all learnings from enrichment scripts
"""
import pandas as pd
import re
import json
from datetime import datetime

def clean_dicho_for_enrichment(dicho):
    """Clean dicho text for enrichment processing"""
    # Remove extra punctuation and normalize
    cleaned = re.sub(r'[^\w\s\.,!?;:\-\(\)]', '', dicho)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = re.sub(r'\s+([.,!?;:])', r'\1', cleaned)
    return cleaned.strip()

def enrich_dicho_with_llm(dicho):
    """
    Simulate LLM enrichment of a dicho
    In a real implementation, this would call an LLM API
    """
    cleaned = clean_dicho_for_enrichment(dicho)
    
    # Simulate LLM analysis based on the dicho content
    enrichment = {
        'dicho': cleaned,
        'translation': generate_translation(cleaned),
        'expanded_context_usage': generate_expanded_context(cleaned),
        'semantic_keywords': generate_semantic_keywords(cleaned),
        'cultural_context': generate_cultural_context(cleaned),
        'emotion_tone': generate_emotion_tone(cleaned),
        'difficulty_level': generate_difficulty_level(cleaned),
        'learning_notes': generate_learning_notes(cleaned)
    }
    
    return enrichment

def generate_translation(dicho):
    """Generate English translation"""
    translations = {
        'Le salió el tiro por la culata': 'The shot came out through the butt (backfired)',
        'más vale toro suelto que lazo debil': 'Better a loose bull than a weak rope',
        'Hablando del rey de Roma y el que se asoma': 'Speaking of the king of Rome and the one who shows up',
        'A buena hambre no hay mal pan': 'To good hunger there is no bad bread',
        'Llovieron perros y gatos y árboles y sombrillas': 'It rained dogs and cats and trees and umbrellas',
        'El Diablo hablando de escapularios': 'The Devil talking about scapulars',
        'Agua que no has de beber déjala correr': 'Water you won\'t drink, let it run',
        'Salió en verso sin mucho esfuerzo': 'It came out in verse without much effort',
        'Arrieros somos y en el camino andamos': 'We are muleteers and we walk the path',
        'Más metido que la pobreza': 'More involved than poverty',
        'Luz de la calle, oscuridad de la casa': 'Light of the street, darkness of the house',
        'El que canta su mal espanta': 'He who sings scares away his troubles',
        'El que llora su mal empeora': 'He who cries makes his troubles worse',
        'Feliz como una lombriz': 'Happy as a worm',
        'A dios rogando y con el mazo dando': 'Praying to God and hitting with the mallet',
        'Tiene más cáscara que un saco de maní': 'Has more shell than a bag of peanuts',
        'Por un oído entra y otro le sale': 'It enters through one ear and leaves through the other',
        'El que por su gusto muere, que lo entierren parado': 'He who dies by his own choice, let them bury him standing',
        'No tiene pelos en la lengua': 'He doesn\'t have hairs on his tongue',
        'En boca cerrada no entran moscas': 'In a closed mouth, flies don\'t enter',
        'Llego por lana y salió trasquilado': 'He came for wool and left sheared',
        'Quien quita un quite': 'Who removes a remove',
        'Se quedó durmiendo en los laureles': 'He stayed sleeping on the laurels',
        'Se le metió el agua': 'The water got into him',
        'Se le corrieron las tejas': 'The tiles ran on him',
        'Los lunes, ni las gallinas ponen': 'On Mondays, not even the hens lay',
        'Voy sentado como Anastacio, con una nalga en el escaño': 'I sit like Anastacio, with one buttock on the bench',
        'Patitas pa\' que te quiero': 'Little feet, what do I want you for',
        'A ojo de buen cubero': 'By eye of a good cooper',
        'Uno más uno, dos; pero la mitad de uno… el hombre': 'One plus one, two; but half of one... the man',
        'No hay peor cuña que la del mismo palo': 'There is no worse wedge than that of the same stick',
        'Las malas conversaciones corrompen las buenas costumbres': 'Bad conversations corrupt good customs',
        'Las mujeres son como las flores, cada año hay nuevas': 'Women are like flowers, each year there are new ones',
        '¡Qué agua fiestas!': 'What party water!',
        'Nunca falta un borracho en una vela': 'There is never a drunk missing at a candle',
        'Sapo verde serás tú': 'You will be a green toad',
        'No hay panza sin ombligo': 'There is no belly without a navel',
        'No hay peor sordo que el que usa walkman': 'There is no worse deaf person than one who uses a walkman',
        'Come santos y caga diablos': 'Eats saints and shits devils',
        'Y qué estaba haciendo, viendo pal icaco': 'And what was he doing, looking at the icaco'
    }
    
    return translations.get(dicho, f'Translation needed for: {dicho}')

def generate_expanded_context(dicho):
    """Generate expanded context and usage examples"""
    contexts = {
        'Le salió el tiro por la culata': 'Used when a plan or action backfires completely. Often said when someone tries to be clever but ends up making things worse.',
        'más vale toro suelto que lazo debil': 'Better to have freedom with some risk than to be constrained by something weak or unreliable.',
        'Hablando del rey de Roma y el que se asoma': 'Said when someone appears just as you were talking about them. Similar to "speak of the devil."',
        'A buena hambre no hay mal pan': 'When you\'re really hungry, any food tastes good. Used to justify eating something simple or not ideal.',
        'Llovieron perros y gatos y árboles y sombrillas': 'Used to describe extremely heavy rain, exaggerating the intensity of the downpour.',
        'El Diablo hablando de escapularios': 'Said when someone gives advice about something they don\'t practice themselves. Like the pot calling the kettle black.',
        'Agua que no has de beber déjala correr': 'Don\'t interfere with things that don\'t concern you. Let things be if they don\'t affect you directly.',
        'Salió en verso sin mucho esfuerzo': 'Something came naturally or easily, without much planning or effort.',
        'Arrieros somos y en el camino andamos': 'We are all travelers on the same path. Used to show solidarity or shared experience.',
        'Más metido que la pobreza': 'Extremely involved or nosy, more than poverty itself (which affects everyone).',
        'Luz de la calle, oscuridad de la casa': 'Someone who appears good in public but is different at home. Public image vs. private reality.',
        'El que canta su mal espanta': 'Singing or being cheerful helps drive away troubles and sadness.',
        'El que llora su mal empeora': 'Crying or dwelling on problems only makes them worse.',
        'Feliz como una lombriz': 'Extremely happy, carefree, and content.',
        'A dios rogando y con el mazo dando': 'Praying to God but also taking action. Faith without works is dead.',
        'Tiene más cáscara que un saco de maní': 'Someone who is very defensive or has many layers of protection.',
        'Por un oído entra y otro le sale': 'Information goes in one ear and out the other. Not paying attention or not retaining information.',
        'El que por su gusto muere, que lo entierren parado': 'If someone chooses to do something dangerous, they should face the consequences.',
        'No tiene pelos en la lengua': 'Someone who speaks directly and honestly, without fear of consequences.',
        'En boca cerrada no entran moscas': 'Keeping quiet prevents trouble. Sometimes it\'s better to say nothing.',
        'Llego por lana y salió trasquilado': 'He came for wool and left sheared. Came looking for something but ended up losing more.',
        'Quien quita un quite': 'Who removes a remove. Used when someone tries to fix something but makes it worse.',
        'Se quedó durmiendo en los laureles': 'He stayed sleeping on the laurels. Resting on past achievements instead of continuing to work.',
        'Se le metió el agua': 'The water got into him. Used when someone gets confused or overwhelmed.',
        'Se le corrieron las tejas': 'The tiles ran on him. Similar to "se le metió el agua" - getting confused or overwhelmed.',
        'Los lunes, ni las gallinas ponen': 'On Mondays, not even the hens lay. Used to express that Mondays are difficult or unproductive.',
        'Voy sentado como Anastacio, con una nalga en el escaño': 'Used to describe someone who is sitting uncomfortably or in an awkward position.',
        'Patitas pa\' que te quiero': 'A playful way to say "little feet, what do I want you for" - expressing affection or teasing.',
        'A ojo de buen cubero': 'By eye of a good cooper - estimating something by sight, without precise measurement.',
        'Uno más uno, dos; pero la mitad de uno… el hombre': 'A philosophical saying about mathematics and human nature.',
        'No hay peor cuña que la del mismo palo': 'There is no worse wedge than that of the same stick - family or close relationships can be the most hurtful.',
        'Las malas conversaciones corrompen las buenas costumbres': 'Bad conversations corrupt good customs - warning about negative influences.',
        'Las mujeres son como las flores, cada año hay nuevas': 'Women are like flowers, each year there are new ones - a somewhat outdated view of relationships.',
        '¡Qué agua fiestas!': 'What party water! - expressing surprise or disbelief about something.',
        'Nunca falta un borracho en una vela': 'There is never a drunk missing at a candle - there\'s always someone who ruins the party.',
        'Sapo verde serás tú': 'You will be a green toad - used to tease someone or call them out.',
        'No hay panza sin ombligo': 'There is no belly without a navel - everything has its origin or cause.',
        'No hay peor sordo que el que usa walkman': 'There is no worse deaf person than one who uses a walkman - someone who chooses not to listen.',
        'Come santos y caga diablos': 'Eats saints and shits devils - someone who appears good but is actually bad.',
        'Y qué estaba haciendo, viendo pal icaco': 'And what was he doing, looking at the icaco - used to express that someone was doing nothing productive.'
    }
    
    return contexts.get(dicho, f'Context needed for: {dicho}')

def generate_semantic_keywords(dicho):
    """Generate semantic keywords for clustering"""
    keywords = {
        'Le salió el tiro por la culata': 'backfire, failure, consequences, plans, mistakes',
        'más vale toro suelto que lazo debil': 'freedom, choice, risk, independence, strength',
        'Hablando del rey de Roma y el que se asoma': 'coincidence, timing, appearance, conversation',
        'A buena hambre no hay mal pan': 'hunger, food, necessity, satisfaction, basic needs',
        'Llovieron perros y gatos y árboles y sombrillas': 'rain, weather, exaggeration, intensity, nature',
        'El Diablo hablando de escapularios': 'hypocrisy, advice, practice, contradiction, religion',
        'Agua que no has de beber déjala correr': 'interference, boundaries, respect, non-involvement',
        'Salió en verso sin mucho esfuerzo': 'natural, easy, poetry, effort, talent',
        'Arrieros somos y en el camino andamos': 'solidarity, journey, shared experience, travelers',
        'Más metido que la pobreza': 'nosy, involved, interference, poverty, social issues',
        'Luz de la calle, oscuridad de la casa': 'appearance, reality, public, private, hypocrisy',
        'El que canta su mal espanta': 'singing, happiness, troubles, music, therapy',
        'El que llora su mal empeora': 'crying, problems, dwelling, sadness, worsening',
        'Feliz como una lombriz': 'happiness, carefree, contentment, nature, simplicity',
        'A dios rogando y con el mazo dando': 'prayer, action, faith, work, religion',
        'Tiene más cáscara que un saco de maní': 'defense, protection, layers, personality, caution',
        'Por un oído entra y otro le sale': 'attention, memory, listening, information, retention',
        'El que por su gusto muere, que lo entierren parado': 'choice, consequences, responsibility, death, standing',
        'No tiene pelos en la lengua': 'honesty, directness, speaking, courage, truth',
        'En boca cerrada no entran moscas': 'silence, wisdom, trouble, speaking, caution',
        'Llego por lana y salió trasquilado': 'loss, gain, wool, shearing, unexpected outcomes',
        'Quien quita un quite': 'fixing, making worse, interference, problems, solutions',
        'Se quedó durmiendo en los laureles': 'rest, achievements, complacency, laurels, past success',
        'Se le metió el agua': 'confusion, overwhelm, water, mental state, problems',
        'Se le corrieron las tejas': 'confusion, overwhelm, tiles, mental state, problems',
        'Los lunes, ni las gallinas ponen': 'Mondays, productivity, difficulty, work, eggs',
        'Voy sentado como Anastacio, con una nalga en el escaño': 'sitting, uncomfortable, position, awkward',
        'Patitas pa\' que te quiero': 'affection, teasing, feet, playful, love',
        'A ojo de buen cubero': 'estimation, sight, measurement, skill, experience',
        'Uno más uno, dos; pero la mitad de uno… el hombre': 'mathematics, philosophy, human nature, counting',
        'No hay peor cuña que la del mismo palo': 'family, relationships, hurt, betrayal, closeness',
        'Las malas conversaciones corrompen las buenas costumbres': 'influence, corruption, conversation, morality',
        'Las mujeres son como las flores, cada año hay nuevas': 'women, relationships, flowers, renewal, outdated',
        '¡Qué agua fiestas!': 'surprise, disbelief, water, parties, expression',
        'Nunca falta un borracho en una vela': 'parties, drunks, disruption, social events',
        'Sapo verde serás tú': 'teasing, toads, green, calling out, humor',
        'No hay panza sin ombligo': 'origin, cause, belly, navel, everything has a source',
        'No hay peor sordo que el que usa walkman': 'deafness, listening, choice, technology, old reference',
        'Come santos y caga diablos': 'hypocrisy, appearance, saints, devils, contradiction',
        'Y qué estaba haciendo, viendo pal icaco': 'doing nothing, icaco, unproductive, lazy, fruit'
    }
    
    return keywords.get(dicho, f'Keywords needed for: {dicho}')

def generate_cultural_context(dicho):
    """Generate cultural context and regional usage"""
    cultural_contexts = {
        'Le salió el tiro por la culata': 'Common in Costa Rica and Central America. Reflects the agricultural and rural culture where firearms were common.',
        'más vale toro suelto que lazo debil': 'Rural Costa Rican wisdom about livestock management. Reflects the importance of cattle in the culture.',
        'Hablando del rey de Roma y el que se asoma': 'Universal Spanish saying, popular throughout Latin America. Shows the influence of European culture.',
        'A buena hambre no hay mal pan': 'Universal Spanish saying about hunger and food. Common in all Spanish-speaking countries.',
        'Llovieron perros y gatos y árboles y sombrillas': 'Costa Rican exaggeration of heavy rain. Reflects the tropical climate and heavy rainfall.',
        'El Diablo hablando de escapularios': 'Religious reference common in Catholic Latin America. Shows the influence of Catholicism.',
        'Agua que no has de beber déjala correr': 'Universal Spanish wisdom about non-interference. Common throughout Latin America.',
        'Salió en verso sin mucho esfuerzo': 'Reflects the poetic and musical culture of Latin America. Common in Costa Rica.',
        'Arrieros somos y en el camino andamos': 'Rural Costa Rican saying about muleteers. Reflects the historical importance of mule transport.',
        'Más metido que la pobreza': 'Costa Rican expression about being nosy. Reflects the social dynamics of small communities.',
        'Luz de la calle, oscuridad de la casa': 'Universal Spanish saying about public vs. private behavior. Common throughout Latin America.',
        'El que canta su mal espanta': 'Universal Spanish saying about music and happiness. Common throughout Latin America.',
        'El que llora su mal empeora': 'Universal Spanish wisdom about dwelling on problems. Common throughout Latin America.',
        'Feliz como una lombriz': 'Costa Rican expression about happiness. Reflects the simple, rural lifestyle.',
        'A dios rogando y con el mazo dando': 'Religious reference common in Catholic Latin America. Shows the influence of Catholicism.',
        'Tiene más cáscara que un saco de maní': 'Costa Rican expression about being defensive. Reflects the local food culture.',
        'Por un oído entra y otro le sale': 'Universal Spanish saying about not paying attention. Common throughout Latin America.',
        'El que por su gusto muere, que lo entierren parado': 'Universal Spanish saying about consequences. Common throughout Latin America.',
        'No tiene pelos en la lengua': 'Universal Spanish saying about honesty. Common throughout Latin America.',
        'En boca cerrada no entran moscas': 'Universal Spanish wisdom about silence. Common throughout Latin America.',
        'Llego por lana y salió trasquilado': 'Rural Costa Rican saying about unexpected outcomes. Reflects the agricultural culture.',
        'Quien quita un quite': 'Costa Rican expression about making things worse. Reflects the local dialect.',
        'Se quedó durmiendo en los laureles': 'Universal Spanish saying about complacency. Common throughout Latin America.',
        'Se le metió el agua': 'Costa Rican expression about confusion. Reflects the local dialect and culture.',
        'Se le corrieron las tejas': 'Costa Rican expression about confusion. Reflects the local dialect and culture.',
        'Los lunes, ni las gallinas ponen': 'Costa Rican expression about Mondays. Reflects the local agricultural culture.',
        'Voy sentado como Anastacio, con una nalga en el escaño': 'Costa Rican expression about uncomfortable sitting. Reflects local culture and humor.',
        'Patitas pa\' que te quiero': 'Costa Rican expression of affection. Reflects the local dialect and endearing language.',
        'A ojo de buen cubero': 'Costa Rican expression about estimation. Reflects the local craftsmanship culture.',
        'Uno más uno, dos; pero la mitad de uno… el hombre': 'Costa Rican philosophical saying. Reflects local wisdom and humor.',
        'No hay peor cuña que la del mismo palo': 'Universal Spanish saying about family relationships. Common throughout Latin America.',
        'Las malas conversaciones corrompen las buenas costumbres': 'Universal Spanish saying about influence. Common throughout Latin America.',
        'Las mujeres son como las flores, cada año hay nuevas': 'Somewhat outdated saying about relationships. Common in traditional Latin American culture.',
        '¡Qué agua fiestas!': 'Costa Rican expression of surprise. Reflects the local dialect and culture.',
        'Nunca falta un borracho en una vela': 'Costa Rican saying about parties. Reflects the local social culture.',
        'Sapo verde serás tú': 'Costa Rican expression for teasing. Reflects the local dialect and humor.',
        'No hay panza sin ombligo': 'Costa Rican saying about origins. Reflects local wisdom and philosophy.',
        'No hay peor sordo que el que usa walkman': 'Costa Rican saying with outdated technology reference. Reflects the time when this was common.',
        'Come santos y caga diablos': 'Costa Rican expression about hypocrisy. Reflects the local religious culture.',
        'Y qué estaba haciendo, viendo pal icaco': 'Costa Rican expression about doing nothing. Reflects the local fruit and culture.'
    }
    
    return cultural_contexts.get(dicho, f'Cultural context needed for: {dicho}')

def generate_emotion_tone(dicho):
    """Generate emotion tone and mood"""
    tones = {
        'Le salió el tiro por la culata': 'ironic, humorous, cautionary',
        'más vale toro suelto que lazo debil': 'wise, philosophical, practical',
        'Hablando del rey de Roma y el que se asoma': 'amused, coincidental, light',
        'A buena hambre no hay mal pan': 'practical, accepting, content',
        'Llovieron perros y gatos y árboles y sombrillas': 'exaggerated, dramatic, humorous',
        'El Diablo hablando de escapularios': 'ironic, critical, humorous',
        'Agua que no has de beber déjala correr': 'wise, cautionary, peaceful',
        'Salió en verso sin mucho esfuerzo': 'pleased, natural, effortless',
        'Arrieros somos y en el camino andamos': 'solidary, philosophical, accepting',
        'Más metido que la pobreza': 'critical, humorous, exasperated',
        'Luz de la calle, oscuridad de la casa': 'critical, observant, wise',
        'El que canta su mal espanta': 'encouraging, positive, therapeutic',
        'El que llora su mal empeora': 'cautionary, practical, wise',
        'Feliz como una lombriz': 'joyful, carefree, content',
        'A dios rogando y con el mazo dando': 'practical, faithful, determined',
        'Tiene más cáscara que un saco de maní': 'observant, critical, humorous',
        'Por un oído entra y otro le sale': 'frustrated, exasperated, resigned',
        'El que por su gusto muere, que lo entierren parado': 'firm, accepting, practical',
        'No tiene pelos en la lengua': 'admiring, respectful, direct',
        'En boca cerrada no entran moscas': 'wise, cautionary, peaceful',
        'Llego por lana y salió trasquilado': 'ironic, humorous, cautionary',
        'Quien quita un quite': 'frustrated, ironic, cautionary',
        'Se quedó durmiendo en los laureles': 'critical, cautionary, wise',
        'Se le metió el agua': 'sympathetic, understanding, humorous',
        'Se le corrieron las tejas': 'sympathetic, understanding, humorous',
        'Los lunes, ni las gallinas ponen': 'resigned, humorous, accepting',
        'Voy sentado como Anastacio, con una nalga en el escaño': 'humorous, descriptive, playful',
        'Patitas pa\' que te quiero': 'affectionate, playful, endearing',
        'A ojo de buen cubero': 'practical, experienced, confident',
        'Uno más uno, dos; pero la mitad de uno… el hombre': 'philosophical, thoughtful, humorous',
        'No hay peor cuña que la del mismo palo': 'wise, cautionary, family-oriented',
        'Las malas conversaciones corrompen las buenas costumbres': 'cautionary, wise, moral',
        'Las mujeres son como las flores, cada año hay nuevas': 'playful, outdated, humorous',
        '¡Qué agua fiestas!': 'surprised, amused, expressive',
        'Nunca falta un borracho en una vela': 'resigned, humorous, social',
        'Sapo verde serás tú': 'teasing, playful, humorous',
        'No hay panza sin ombligo': 'philosophical, wise, thoughtful',
        'No hay peor sordo que el que usa walkman': 'frustrated, humorous, outdated',
        'Come santos y caga diablos': 'critical, ironic, humorous',
        'Y qué estaba haciendo, viendo pal icaco': 'playful, humorous, descriptive'
    }
    
    return tones.get(dicho, f'Tone needed for: {dicho}')

def generate_difficulty_level(dicho):
    """Generate difficulty level for learning"""
    difficulty_levels = {
        'Le salió el tiro por la culata': 'intermediate',
        'más vale toro suelto que lazo debil': 'advanced',
        'Hablando del rey de Roma y el que se asoma': 'beginner',
        'A buena hambre no hay mal pan': 'beginner',
        'Llovieron perros y gatos y árboles y sombrillas': 'intermediate',
        'El Diablo hablando de escapularios': 'advanced',
        'Agua que no has de beber déjala correr': 'intermediate',
        'Salió en verso sin mucho esfuerzo': 'intermediate',
        'Arrieros somos y en el camino andamos': 'intermediate',
        'Más metido que la pobreza': 'advanced',
        'Luz de la calle, oscuridad de la casa': 'intermediate',
        'El que canta su mal espanta': 'beginner',
        'El que llora su mal empeora': 'beginner',
        'Feliz como una lombriz': 'beginner',
        'A dios rogando y con el mazo dando': 'advanced',
        'Tiene más cáscara que un saco de maní': 'advanced',
        'Por un oído entra y otro le sale': 'intermediate',
        'El que por su gusto muere, que lo entierren parado': 'advanced',
        'No tiene pelos en la lengua': 'intermediate',
        'En boca cerrada no entran moscas': 'intermediate',
        'Llego por lana y salió trasquilado': 'advanced',
        'Quien quita un quite': 'advanced',
        'Se quedó durmiendo en los laureles': 'intermediate',
        'Se le metió el agua': 'intermediate',
        'Se le corrieron las tejas': 'intermediate',
        'Los lunes, ni las gallinas ponen': 'beginner',
        'Voy sentado como Anastacio, con una nalga en el escaño': 'advanced',
        'Patitas pa\' que te quiero': 'intermediate',
        'A ojo de buen cubero': 'advanced',
        'Uno más uno, dos; pero la mitad de uno… el hombre': 'advanced',
        'No hay peor cuña que la del mismo palo': 'intermediate',
        'Las malas conversaciones corrompen las buenas costumbres': 'advanced',
        'Las mujeres son como las flores, cada año hay nuevas': 'intermediate',
        '¡Qué agua fiestas!': 'beginner',
        'Nunca falta un borracho en una vela': 'intermediate',
        'Sapo verde serás tú': 'intermediate',
        'No hay panza sin ombligo': 'intermediate',
        'No hay peor sordo que el que usa walkman': 'intermediate',
        'Come santos y caga diablos': 'advanced',
        'Y qué estaba haciendo, viendo pal icaco': 'intermediate'
    }
    
    return difficulty_levels.get(dicho, 'intermediate')

def generate_learning_notes(dicho):
    """Generate learning notes and tips"""
    learning_notes = {
        'Le salió el tiro por la culata': 'Use when plans backfire. Great for expressing irony and consequences.',
        'más vale toro suelto que lazo debil': 'Philosophical saying about freedom vs. constraint. Use in discussions about choice.',
        'Hablando del rey de Roma y el que se asoma': 'Perfect for coincidences. Similar to "speak of the devil" in English.',
        'A buena hambre no hay mal pan': 'Simple and practical. Great for beginners learning about hunger and food.',
        'Llovieron perros y gatos y árboles y sombrillas': 'Fun exaggeration. Great for describing heavy rain humorously.',
        'El Diablo hablando de escapularios': 'Use when someone gives advice they don\'t follow. Shows hypocrisy.',
        'Agua que no has de beber déjala correr': 'Wise advice about non-interference. Use when someone is too nosy.',
        'Salió en verso sin mucho esfuerzo': 'Use when something comes naturally. Great for describing talent or ease.',
        'Arrieros somos y en el camino andamos': 'Show solidarity and shared experience. Use to connect with others.',
        'Más metido que la pobreza': 'Use when someone is extremely nosy. Great for expressing frustration.',
        'Luz de la calle, oscuridad de la casa': 'Use to describe someone who appears different in public vs. private.',
        'El que canta su mal espanta': 'Encouraging saying about music and happiness. Use to cheer someone up.',
        'El que llora su mal empeora': 'Practical advice about dwelling on problems. Use to encourage action.',
        'Feliz como una lombriz': 'Express extreme happiness. Great for describing contentment and joy.',
        'A dios rogando y con el mazo dando': 'Show the importance of both faith and action. Use in religious contexts.',
        'Tiene más cáscara que un saco de maní': 'Describe someone who is very defensive. Use to express frustration.',
        'Por un oído entra y otro le sale': 'Express frustration with someone not listening. Use when someone ignores advice.',
        'El que por su gusto muere, que lo entierren parado': 'Accept consequences of choices. Use when someone makes a bad decision.',
        'No tiene pelos en la lengua': 'Praise someone for being honest and direct. Use to express admiration.',
        'En boca cerrada no entran moscas': 'Advise silence and caution. Use when someone is talking too much.',
        'Llego por lana y salió trasquilado': 'Describe unexpected negative outcomes. Use when someone loses more than they gained.',
        'Quien quita un quite': 'Express frustration with someone making things worse. Use when someone interferes poorly.',
        'Se quedó durmiendo en los laureles': 'Warn against complacency. Use when someone rests on past achievements.',
        'Se le metió el agua': 'Describe confusion or overwhelm. Use when someone gets lost or confused.',
        'Se le corrieron las tejas': 'Describe confusion or overwhelm. Use when someone gets lost or confused.',
        'Los lunes, ni las gallinas ponen': 'Express Monday difficulties. Use to complain about Mondays humorously.',
        'Voy sentado como Anastacio, con una nalga en el escaño': 'Describe uncomfortable sitting. Use humorously to describe awkward positions.',
        'Patitas pa\' que te quiero': 'Express affection playfully. Use with close friends or family in a teasing way.',
        'A ojo de buen cubero': 'Express estimation by sight. Use when making rough calculations or estimates.',
        'Uno más uno, dos; pero la mitad de uno… el hombre': 'Philosophical comment about mathematics and human nature. Use in thoughtful discussions.',
        'No hay peor cuña que la del mismo palo': 'Warn about family or close relationships being hurtful. Use when discussing family dynamics.',
        'Las malas conversaciones corrompen las buenas costumbres': 'Warn about negative influences. Use when discussing the impact of bad company.',
        'Las mujeres son como las flores, cada año hay nuevas': 'Outdated saying about relationships. Use carefully as it may be considered sexist.',
        '¡Qué agua fiestas!': 'Express surprise or disbelief. Use when something unexpected happens.',
        'Nunca falta un borracho en una vela': 'Complain about party disruptors. Use when someone ruins a social event.',
        'Sapo verde serás tú': 'Tease someone playfully. Use with friends in a humorous way.',
        'No hay panza sin ombligo': 'Express that everything has an origin. Use in philosophical discussions.',
        'No hay peor sordo que el que usa walkman': 'Express frustration with someone not listening. Use when someone ignores advice.',
        'Come santos y caga diablos': 'Describe hypocrisy. Use when someone appears good but is actually bad.',
        'Y qué estaba haciendo, viendo pal icaco': 'Describe doing nothing productive. Use humorously to describe laziness or inactivity.'
    }
    
    return learning_notes.get(dicho, f'Learning notes needed for: {dicho}')

def enrich_dichos_from_file(input_file, output_file):
    """Enrich dichos from a TSV file and save the results"""
    print("🚀 Enriching Dichos with LLM Analysis")
    print("=" * 60)
    
    # Load unique dichos
    try:
        df = pd.read_csv(input_file, sep='\t')
        print(f"📚 Loaded {len(df)} dichos for enrichment")
    except FileNotFoundError:
        print(f"❌ Error: {input_file} not found")
        return
    
    # Enrich each dicho
    enriched_dichos = []
    
    for i, row in df.iterrows():
        dicho = row['cleaned']
        print(f"🔍 Enriching: {dicho}")
        
        enrichment = enrich_dicho_with_llm(dicho)
        
        # Add original metadata
        enrichment['original'] = row.get('original', dicho)
        enrichment['date_time'] = row.get('date_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        enrichment['contributor_first'] = row.get('contributor', 'Unknown')
        enrichment['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        enrichment['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        enriched_dichos.append(enrichment)
    
    # Create enriched DataFrame
    enriched_df = pd.DataFrame(enriched_dichos)
    
    # Save enriched dichos
    enriched_df.to_csv(output_file, sep='\t', index=False)
    
    print(f"\n✅ Enrichment complete!")
    print(f"📊 Enriched {len(enriched_df)} dichos")
    print(f"💾 Saved to: {output_file}")
    
    # Show sample of enriched data
    print(f"\n📝 SAMPLE ENRICHED DICHOS:")
    for i, row in enriched_df.head(3).iterrows():
        print(f"\n{i+1}. {row['dicho']}")
        print(f"   Translation: {row['translation']}")
        print(f"   Context: {row['expanded_context_usage'][:100]}...")
        print(f"   Keywords: {row['semantic_keywords']}")
        print(f"   Tone: {row['emotion_tone']}")

def main():
    """Main function for command-line usage"""
    enrich_dichos_from_file('unique_new_dichos.tsv', 'enriched_new_dichos.tsv')

if __name__ == "__main__":
    main()

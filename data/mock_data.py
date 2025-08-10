"""
Comprehensive Mock Data Infrastructure for CarIActerology
Based on René Le Senne's characterology framework
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
import random

# René Le Senne's 8 Character Types
CHARACTER_TYPES = {
    "nervous": {
        "name": "Nervous (nE-nA-P)",
        "traits": {"emotionality": 8.2, "activity": 3.1, "resonance": 2.4},
        "description": "Highly emotional, low activity, primary resonance. Quick to react, imaginative, but lacks persistence.",
        "strengths": ["Creative", "Intuitive", "Empathetic", "Artistic"],
        "challenges": ["Impulsive", "Inconsistent", "Oversensitive", "Unfocused"],
        "color": "#FF6B6B"
    },
    "sentimental": {
        "name": "Sentimental (E-nA-S)",
        "traits": {"emotionality": 8.7, "activity": 2.9, "resonance": 8.1},
        "description": "Very emotional, low activity, secondary resonance. Deep feelings, memory-driven, introspective.",
        "strengths": ["Deep thinker", "Loyal", "Compassionate", "Reflective"],
        "challenges": ["Melancholic", "Dwelling on past", "Withdrawn", "Pessimistic"],
        "color": "#4ECDC4"
    },
    "choleric": {
        "name": "Choleric (E-A-P)",
        "traits": {"emotionality": 7.9, "activity": 8.8, "resonance": 2.8},
        "description": "Emotional, very active, primary resonance. Energetic leaders, quick decisions, action-oriented.",
        "strengths": ["Leadership", "Dynamic", "Decisive", "Passionate"],
        "challenges": ["Impatient", "Aggressive", "Impulsive", "Domineering"],
        "color": "#FF9F43"
    },
    "passionate": {
        "name": "Passionate (E-A-S)",
        "traits": {"emotionality": 8.9, "activity": 8.6, "resonance": 8.5},
        "description": "Very emotional, very active, secondary resonance. Intense, driven, all-or-nothing approach.",
        "strengths": ["Intense focus", "Determined", "Inspiring", "Committed"],
        "challenges": ["Obsessive", "Inflexible", "Extreme", "Burnout-prone"],
        "color": "#E74C3C"
    },
    "sanguine": {
        "name": "Sanguine (nE-A-P)",
        "traits": {"emotionality": 3.2, "activity": 8.3, "resonance": 2.7},
        "description": "Low emotionality, very active, primary resonance. Optimistic, practical, socially active.",
        "strengths": ["Optimistic", "Practical", "Social", "Adaptable"],
        "challenges": ["Superficial", "Inconsistent", "Avoids depth", "Restless"],
        "color": "#F39C12"
    },
    "phlegmatic": {
        "name": "Phlegmatic (nE-A-S)",
        "traits": {"emotionality": 2.8, "activity": 8.1, "resonance": 7.9},
        "description": "Low emotionality, very active, secondary resonance. Calm, methodical, persistent workers.",
        "strengths": ["Calm", "Methodical", "Reliable", "Persistent"],
        "challenges": ["Unemotional", "Rigid", "Slow to change", "Indifferent"],
        "color": "#27AE60"
    },
    "amorphous": {
        "name": "Amorphous (nE-nA-P)",
        "traits": {"emotionality": 2.5, "activity": 2.4, "resonance": 2.1},
        "description": "Low emotionality, low activity, primary resonance. Easy-going but lacks direction and drive.",
        "strengths": ["Easy-going", "Peaceful", "Flexible", "Non-confrontational"],
        "challenges": ["Lacks direction", "Passive", "Unmotivated", "Dependent"],
        "color": "#95A5A6"
    },
    "apathetic": {
        "name": "Apathetic (nE-nA-S)",
        "traits": {"emotionality": 2.2, "activity": 2.6, "resonance": 7.8},
        "description": "Low emotionality, low activity, secondary resonance. Detached, intellectual, avoids involvement.",
        "strengths": ["Analytical", "Objective", "Independent", "Rational"],
        "challenges": ["Detached", "Cold", "Pessimistic", "Isolated"],
        "color": "#7F8C8D"
    }
}

def get_mock_user_profile() -> Dict[str, Any]:
    """Generate a comprehensive mock user profile"""
    
    # Primary character type (weighted random selection)
    primary_type = random.choices(
        list(CHARACTER_TYPES.keys()),
        weights=[15, 12, 14, 10, 16, 13, 12, 8]  # More common types weighted higher
    )[0]
    
    # Secondary influences (2-3 other types with lower confidence)
    secondary_types = random.sample(
        [t for t in CHARACTER_TYPES.keys() if t != primary_type], 
        k=random.randint(1, 2)
    )
    
    return {
        "user_id": "user_001",
        "primary_type": primary_type,
        "secondary_influences": secondary_types,
        "confidence_score": round(random.uniform(0.72, 0.94), 2),
        "analysis_sessions": random.randint(15, 45),
        "total_interactions": random.randint(150, 500),
        "member_since": datetime.now() - timedelta(days=random.randint(30, 365)),
        "last_session": datetime.now() - timedelta(hours=random.randint(2, 72)),
        "growth_trajectory": random.choice(["improving", "stable", "exploring", "developing"]),
        "key_insights_count": random.randint(8, 25)
    }

def get_mock_session_history(days: int = 30) -> List[Dict[str, Any]]:
    """Generate mock session history for analysis"""
    sessions = []
    
    for i in range(random.randint(8, 20)):
        session_date = datetime.now() - timedelta(days=random.randint(1, days))
        
        # Generate realistic session data
        session = {
            "session_id": f"session_{i+1:03d}",
            "date": session_date,
            "duration_minutes": random.randint(15, 90),
            "messages_exchanged": random.randint(12, 45),
            "insights_discovered": random.randint(1, 5),
            "mood_rating": round(random.uniform(3.2, 8.7), 1),
            "session_type": random.choice([
                "character_exploration", "trait_analysis", "behavioral_patterns", 
                "emotional_mapping", "goal_setting", "progress_review"
            ]),
            "key_topics": random.sample([
                "emotional_patterns", "decision_making", "relationships", "work_style",
                "stress_response", "communication", "leadership", "creativity",
                "motivation", "conflict_resolution", "personal_growth", "values"
            ], k=random.randint(2, 4)),
            "breakthrough_moments": random.randint(0, 2),
            "homework_assigned": random.choice([True, False]),
            "satisfaction_score": round(random.uniform(7.2, 9.8), 1)
        }
        sessions.append(session)
    
    return sorted(sessions, key=lambda x: x['date'], reverse=True)

def get_mock_insights_gallery() -> List[Dict[str, Any]]:
    """Generate a gallery of psychological insights discovered"""
    
    insight_templates = [
        {
            "category": "Emotional Patterns",
            "insights": [
                "You tend to process emotions more deeply when given time to reflect",
                "Your emotional responses are strongest in social contexts",
                "You show remarkable emotional resilience during challenging periods",
                "Your empathy levels peak when helping others work through problems"
            ]
        },
        {
            "category": "Decision Making", 
            "insights": [
                "You prefer collaborative decision-making over solo choices",
                "Your best decisions come when you balance logic with intuition",
                "You tend to overthink decisions involving potential conflict",
                "Your risk tolerance increases when pursuing creative projects"
            ]
        },
        {
            "category": "Interpersonal Style",
            "insights": [
                "You naturally adapt your communication style to your audience",
                "You're energized by meaningful one-on-one conversations",
                "You tend to avoid confrontation but address issues indirectly",
                "Your leadership style is more facilitative than directive"
            ]
        },
        {
            "category": "Work & Productivity",
            "insights": [
                "Your productivity peaks in collaborative environments",
                "You need variety in your work to maintain engagement",
                "You perform best when work aligns with your personal values",
                "You benefit from regular feedback and recognition"
            ]
        },
        {
            "category": "Stress & Coping",
            "insights": [
                "You cope with stress through creative expression and reflection",
                "Your stress levels decrease when you have clear priorities",
                "You recharge best through solitude and nature",
                "You handle uncertainty better when you focus on what you can control"
            ]
        }
    ]
    
    insights = []
    for category_data in insight_templates:
        category_insights = random.sample(category_data["insights"], k=random.randint(2, 4))
        for insight_text in category_insights:
            insights.append({
                "insight_id": f"insight_{len(insights)+1:03d}",
                "category": category_data["category"],
                "text": insight_text,
                "discovered_date": datetime.now() - timedelta(days=random.randint(1, 60)),
                "confidence": round(random.uniform(0.75, 0.95), 2),
                "validation_count": random.randint(1, 8),
                "related_sessions": random.randint(2, 6),
                "actionable": random.choice([True, False]),
                "priority": random.choice(["high", "medium", "low"])
            })
    
    return sorted(insights, key=lambda x: x['discovered_date'], reverse=True)

def get_mock_conversation_history() -> List[Dict[str, Any]]:
    """Generate realistic conversation history"""
    
    conversation_starters = [
        "I've been feeling overwhelmed at work lately and I'm not sure how to handle it.",
        "I notice I react differently in group settings versus one-on-one conversations.",
        "I'm curious about why I procrastinate on certain types of tasks but not others.",
        "I've been reflecting on my relationships and notice some patterns I'd like to understand.",
        "I feel like I'm at a crossroads in my life and need to understand my decision-making process.",
        "I'm interested in understanding my leadership style and how others perceive me.",
        "I've noticed I have different energy levels throughout the day and wonder what drives this.",
        "I'd like to explore why certain situations trigger anxiety while others don't."
    ]
    
    ai_response_templates = [
        "That's a fascinating observation about {topic}. In characterology, we often see that {insight}. Can you tell me more about when you first noticed this pattern?",
        "Your experience with {topic} suggests some interesting aspects of your character structure. According to Le Senne's framework, this could indicate {trait}. How does this resonate with your self-perception?",
        "I notice some intriguing patterns emerging from what you've shared about {topic}. This aligns with characteristics we see in {character_type} types. What situations bring out this aspect of your personality most strongly?",
        "Thank you for sharing your experience with {topic}. Your openness to self-exploration is remarkable. I'm seeing potential connections to {psychological_concept}. How would you describe your approach to {related_area}?",
        "This insight about {topic} is very revealing. In my analysis, I'm noticing indicators of {trait_pattern}. This could explain why you {behavior}. Have you noticed this pattern in other areas of your life?"
    ]
    
    conversations = []
    for i in range(random.randint(20, 40)):
        topic = random.choice(["stress management", "decision-making", "relationships", "work dynamics", "personal growth", "emotional responses"])
        
        user_message = random.choice(conversation_starters)
        ai_response = random.choice(ai_response_templates).format(
            topic=topic,
            insight=random.choice(["emotional patterns vary significantly between individuals", "activity levels correlate with resonance patterns", "secondary traits often emerge under stress"]),
            trait=random.choice(["higher emotional resonance", "strong activity orientation", "complex emotional patterns"]),
            character_type=random.choice(list(CHARACTER_TYPES.keys())),
            psychological_concept=random.choice(["emotional intelligence", "cognitive flexibility", "stress response patterns"]),
            trait_pattern=random.choice(["emotional-active orientation", "reflective processing style", "adaptive leadership tendencies"]),
            behavior=random.choice(["prefer collaborative approaches", "need processing time", "thrive in structured environments"]),
            related_area=random.choice(["work relationships", "personal goals", "creative expression", "conflict resolution"])
        )
        
        conversations.append({
            "conversation_id": f"conv_{i+1:03d}",
            "timestamp": datetime.now() - timedelta(hours=random.randint(1, 720)),
            "user_message": user_message,
            "ai_response": ai_response,
            "message_type": random.choice(["exploration", "analysis", "insight", "clarification", "validation"]),
            "sentiment": random.choice(["curious", "reflective", "concerned", "hopeful", "analytical"]),
            "topics_tagged": random.sample([topic, "character_analysis", "self_discovery"], k=2),
            "insights_generated": random.randint(0, 3),
            "user_engagement": round(random.uniform(0.6, 0.95), 2)
        })
    
    return sorted(conversations, key=lambda x: x['timestamp'], reverse=True)

def get_mock_progress_metrics() -> Dict[str, Any]:
    """Generate progress tracking metrics"""
    
    return {
        "overall_progress": {
            "self_awareness_score": round(random.uniform(6.8, 9.2), 1),
            "emotional_intelligence": round(random.uniform(7.1, 8.9), 1),
            "decision_making_confidence": round(random.uniform(6.5, 8.8), 1),
            "interpersonal_effectiveness": round(random.uniform(7.0, 9.1), 1),
            "stress_management": round(random.uniform(6.2, 8.7), 1),
            "goal_clarity": round(random.uniform(7.3, 9.0), 1)
        },
        "weekly_progress": [
            {
                "week": f"Week {i+1}",
                "date": datetime.now() - timedelta(weeks=i),
                "insights_gained": random.randint(2, 8),
                "session_quality": round(random.uniform(7.0, 9.5), 1),
                "engagement_score": round(random.uniform(0.75, 0.98), 2),
                "breakthrough_moments": random.randint(0, 2),
                "homework_completion": round(random.uniform(0.6, 1.0), 2)
            }
            for i in range(12)
        ],
        "milestone_achievements": [
            {
                "milestone": "First Character Type Identification",
                "achieved_date": datetime.now() - timedelta(days=random.randint(20, 60)),
                "description": "Successfully identified primary character type with high confidence"
            },
            {
                "milestone": "Emotional Pattern Recognition",
                "achieved_date": datetime.now() - timedelta(days=random.randint(15, 45)),
                "description": "Recognized and named key emotional patterns in daily life"
            },
            {
                "milestone": "Interpersonal Insight Breakthrough",
                "achieved_date": datetime.now() - timedelta(days=random.randint(10, 30)),
                "description": "Major insight into relationship dynamics and communication style"
            },
            {
                "milestone": "Decision-Making Framework",
                "achieved_date": datetime.now() - timedelta(days=random.randint(5, 20)),
                "description": "Developed personal framework for making difficult decisions"
            }
        ],
        "growth_areas": [
            {
                "area": "Emotional Regulation",
                "current_level": round(random.uniform(6.5, 8.5), 1),
                "target_level": 9.0,
                "progress_percentage": round(random.uniform(65, 85), 1),
                "next_steps": ["Practice mindfulness techniques", "Identify triggers", "Develop coping strategies"]
            },
            {
                "area": "Communication Skills",
                "current_level": round(random.uniform(7.0, 8.8), 1),
                "target_level": 9.2,
                "progress_percentage": round(random.uniform(70, 90), 1),
                "next_steps": ["Active listening practice", "Assertiveness training", "Feedback solicitation"]
            },
            {
                "area": "Leadership Development",
                "current_level": round(random.uniform(6.8, 8.2), 1),
                "target_level": 8.8,
                "progress_percentage": round(random.uniform(68, 82), 1),
                "next_steps": ["Leadership style assessment", "Team dynamics study", "Mentorship opportunities"]
            }
        ]
    }

def get_mock_recommendations() -> List[Dict[str, Any]]:
    """Generate therapeutic recommendations and suggestions"""
    
    recommendations = [
        {
            "id": "rec_001",
            "category": "Emotional Development",
            "title": "Daily Emotion Journaling",
            "description": "Spend 10 minutes each evening reflecting on and writing about your emotional experiences from the day.",
            "rationale": "Based on your character type, regular emotional processing will enhance self-awareness and emotional regulation.",
            "difficulty": "Easy",
            "time_commitment": "10 minutes daily",
            "expected_benefits": ["Improved emotional awareness", "Better stress management", "Enhanced self-reflection"],
            "priority": "high",
            "personalised_note": "This practice aligns perfectly with your reflective nature and will support your secondary resonance patterns."
        },
        {
            "id": "rec_002",
            "category": "Interpersonal Skills",
            "title": "Communication Style Adaptation",
            "description": "Practice identifying others' communication preferences and adapting your style accordingly in one interaction daily.",
            "rationale": "Your natural empathy combined with communication skill development will enhance relationship effectiveness.",
            "difficulty": "Medium",
            "time_commitment": "Ongoing practice",
            "expected_benefits": ["Improved relationships", "Better collaboration", "Reduced conflicts"],
            "priority": "medium",
            "personalised_note": "Your character type thrives in collaborative environments, making this a natural growth area."
        },
        {
            "id": "rec_003", 
            "category": "Decision Making",
            "title": "Values-Based Decision Framework",
            "description": "Create a personal decision-making framework that prioritizes your core values and long-term goals.",
            "rationale": "Aligning decisions with values reduces internal conflict and increases satisfaction with outcomes.",
            "difficulty": "Medium",
            "time_commitment": "2-3 hours setup, then ongoing use",
            "expected_benefits": ["Clearer decision-making", "Reduced decision fatigue", "Better life alignment"],
            "priority": "high",
            "personalised_note": "Your secondary resonance pattern means you naturally consider long-term implications, making this approach ideal."
        },
        {
            "id": "rec_004",
            "category": "Stress Management",
            "title": "Nature-Based Restoration",
            "description": "Schedule 30 minutes of outdoor time daily, preferably in natural settings, for mental restoration.",
            "rationale": "Your character profile indicates you recharge through solitude and connection with nature.",
            "difficulty": "Easy",
            "time_commitment": "30 minutes daily",
            "expected_benefits": ["Reduced stress", "Improved focus", "Enhanced creativity"],
            "priority": "medium",
            "personalised_note": "This aligns with your need for peaceful environments to process emotions and thoughts."
        }
    ]
    
    return recommendations

def get_mock_therapeutic_themes() -> Dict[str, Any]:
    """Generate therapeutic themes and focus areas"""
    
    return {
        "current_themes": [
            {
                "theme": "Authentic Self-Expression",
                "description": "Exploring ways to express your true self in various life contexts",
                "sessions_focused": random.randint(3, 8),
                "progress_level": round(random.uniform(6.5, 8.5), 1),
                "key_insights": [
                    "Authenticity increases when you feel psychologically safe",
                    "Your self-expression varies significantly across different relationships",
                    "Creative outlets serve as important channels for authentic expression"
                ]
            },
            {
                "theme": "Relationship Dynamics",
                "description": "Understanding patterns in your interpersonal relationships",
                "sessions_focused": random.randint(4, 10),
                "progress_level": round(random.uniform(7.0, 9.0), 1),
                "key_insights": [
                    "You tend to attract people who appreciate your empathetic nature",
                    "Conflict avoidance sometimes prevents deeper intimacy",
                    "Your listening skills are a significant strength in relationships"
                ]
            },
            {
                "theme": "Career Alignment",
                "description": "Aligning career choices with your character type and values",
                "sessions_focused": random.randint(2, 6),
                "progress_level": round(random.uniform(6.0, 8.0), 1),
                "key_insights": [
                    "You thrive in environments that value collaboration over competition",
                    "Meaningful work is more important to you than high compensation",
                    "You need variety and creativity in your professional role"
                ]
            }
        ],
        "completed_themes": [
            {
                "theme": "Emotional Intelligence Development",
                "description": "Building awareness and management of emotional responses",
                "completion_date": datetime.now() - timedelta(days=random.randint(30, 90)),
                "final_score": round(random.uniform(8.0, 9.5), 1),
                "key_achievements": [
                    "Identified personal emotional triggers",
                    "Developed healthy coping strategies",
                    "Improved emotional communication with others"
                ]
            }
        ],
        "upcoming_themes": [
            {
                "theme": "Leadership Style Development",
                "description": "Exploring and developing your natural leadership approach",
                "planned_start": datetime.now() + timedelta(days=random.randint(7, 21)),
                "expected_duration": "6-8 sessions",
                "rationale": "Building on your interpersonal strengths to develop leadership capabilities"
            }
        ]
    }

# Utility functions for easy data access
def get_primary_character_type() -> Dict[str, Any]:
    """Get the user's primary character type data"""
    profile = get_mock_user_profile()
    return CHARACTER_TYPES[profile["primary_type"]]

def get_character_evolution_data(months: int = 6) -> List[Dict[str, Any]]:
    """Generate character trait evolution over time"""
    primary_type = get_primary_character_type()
    base_traits = primary_type["traits"]
    
    evolution = []
    for i in range(months):
        date = datetime.now() - timedelta(days=30 * (months - i))
        
        # Simulate gradual character development
        traits = {
            trait: max(0, min(10, base_traits[trait] + random.uniform(-0.5, 0.8)))
            for trait in base_traits
        }
        
        evolution.append({
            "date": date,
            "traits": traits,
            "confidence": round(random.uniform(0.65, 0.95), 2),
            "major_events": random.choice([
                [], 
                ["Career transition"], 
                ["Relationship change"], 
                ["Personal insight breakthrough"],
                ["Stress period", "Recovery phase"]
            ])
        })
    
    return evolution

# Export all mock data functions
__all__ = [
    'CHARACTER_TYPES',
    'get_mock_user_profile',
    'get_mock_session_history', 
    'get_mock_insights_gallery',
    'get_mock_conversation_history',
    'get_mock_progress_metrics',
    'get_mock_recommendations',
    'get_mock_therapeutic_themes',
    'get_primary_character_type',
    'get_character_evolution_data'
]
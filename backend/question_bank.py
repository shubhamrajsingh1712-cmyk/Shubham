# Comprehensive Question Bank for Psychometric Assessment
# Total: 200 questions (40 per dimension)

QUESTION_BANK = {
    "orientation": {
        "title": "Work Orientation & Style Assessment",
        "description": "This section evaluates your preferred work style and orientation towards different types of tasks and environments.",
        "questions": [
            # Creative Orientation (10 questions)
            {"id": "orient_creative_1", "text": "I enjoy working on creative projects that allow me to express my ideas", "category": "creative", "reverse": False},
            {"id": "orient_creative_2", "text": "I find satisfaction in designing visual or artistic content", "category": "creative", "reverse": False},
            {"id": "orient_creative_3", "text": "I prefer jobs that allow me to think outside the box", "category": "creative", "reverse": False},
            {"id": "orient_creative_4", "text": "I enjoy brainstorming innovative solutions to problems", "category": "creative", "reverse": False},
            {"id": "orient_creative_5", "text": "I like experimenting with new ideas and approaches", "category": "creative", "reverse": False},
            {"id": "orient_creative_6", "text": "I feel energized when working on artistic or design projects", "category": "creative", "reverse": False},
            {"id": "orient_creative_7", "text": "I prefer tasks that require imagination and originality", "category": "creative", "reverse": False},
            {"id": "orient_creative_8", "text": "I enjoy expressing myself through creative mediums", "category": "creative", "reverse": False},
            {"id": "orient_creative_9", "text": "I would rather follow established procedures than create new ones", "category": "creative", "reverse": True},
            {"id": "orient_creative_10", "text": "I find routine, repetitive creative work fulfilling", "category": "creative", "reverse": False},
            
            # Analytical Orientation (10 questions)
            {"id": "orient_analytical_1", "text": "I prefer solving logical puzzles and analyzing data", "category": "analytical", "reverse": False},
            {"id": "orient_analytical_2", "text": "I am good at mathematical calculations and problem-solving", "category": "analytical", "reverse": False},
            {"id": "orient_analytical_3", "text": "I enjoy working with numbers and statistical information", "category": "analytical", "reverse": False},
            {"id": "orient_analytical_4", "text": "I like breaking down complex problems into smaller parts", "category": "analytical", "reverse": False},
            {"id": "orient_analytical_5", "text": "I prefer making decisions based on data and facts", "category": "analytical", "reverse": False},
            {"id": "orient_analytical_6", "text": "I enjoy researching and investigating topics in depth", "category": "analytical", "reverse": False},
            {"id": "orient_analytical_7", "text": "I find satisfaction in identifying patterns and trends", "category": "analytical", "reverse": False},
            {"id": "orient_analytical_8", "text": "I prefer systematic, methodical approaches to work", "category": "analytical", "reverse": False},
            {"id": "orient_analytical_9", "text": "I enjoy testing hypotheses and drawing conclusions", "category": "analytical", "reverse": False},
            {"id": "orient_analytical_10", "text": "I rely on intuition rather than data when making decisions", "category": "analytical", "reverse": True},
            
            # People-Centric Orientation (10 questions)
            {"id": "orient_people_1", "text": "I like helping others and working in team environments", "category": "people_centric", "reverse": False},
            {"id": "orient_people_2", "text": "I prefer working with people rather than working alone", "category": "people_centric", "reverse": False},
            {"id": "orient_people_3", "text": "I enjoy teaching and mentoring others", "category": "people_centric", "reverse": False},
            {"id": "orient_people_4", "text": "I feel fulfilled when I can make a positive impact on others", "category": "people_centric", "reverse": False},
            {"id": "orient_people_5", "text": "I prefer collaborative work over individual tasks", "category": "people_centric", "reverse": False},
            {"id": "orient_people_6", "text": "I enjoy facilitating discussions and group activities", "category": "people_centric", "reverse": False},
            {"id": "orient_people_7", "text": "I am energized by social interactions at work", "category": "people_centric", "reverse": False},
            {"id": "orient_people_8", "text": "I like careers that involve direct service to others", "category": "people_centric", "reverse": False},
            {"id": "orient_people_9", "text": "I prefer solving people-related problems over technical ones", "category": "people_centric", "reverse": False},
            {"id": "orient_people_10", "text": "I would rather work independently than in a team", "category": "people_centric", "reverse": True},
            
            # Administrative Orientation (10 questions)
            {"id": "orient_admin_1", "text": "I enjoy organizing tasks and following structured processes", "category": "administrative", "reverse": False},
            {"id": "orient_admin_2", "text": "I like maintaining order and managing documentation", "category": "administrative", "reverse": False},
            {"id": "orient_admin_3", "text": "I prefer clear guidelines and well-defined procedures", "category": "administrative", "reverse": False},
            {"id": "orient_admin_4", "text": "I find satisfaction in creating systems and workflows", "category": "administrative", "reverse": False},
            {"id": "orient_admin_5", "text": "I enjoy planning and coordinating activities", "category": "administrative", "reverse": False},
            {"id": "orient_admin_6", "text": "I am comfortable with detailed record-keeping", "category": "administrative", "reverse": False},
            {"id": "orient_admin_7", "text": "I prefer predictable, well-structured work environments", "category": "administrative", "reverse": False},
            {"id": "orient_admin_8", "text": "I like implementing and maintaining organizational systems", "category": "administrative", "reverse": False},
            {"id": "orient_admin_9", "text": "I enjoy managing schedules and timelines", "category": "administrative", "reverse": False},
            {"id": "orient_admin_10", "text": "I prefer spontaneous, unstructured work over planned tasks", "category": "administrative", "reverse": True},
        ]
    },
    
    "interest": {
        "title": "Interest Mapping Assessment",
        "description": "This section identifies your natural interests and areas of curiosity across various domains.",
        "questions": [
            # STEM Interests (8 questions)
            {"id": "interest_stem_1", "text": "I am fascinated by how things work mechanically", "category": "stem", "reverse": False},
            {"id": "interest_stem_2", "text": "I enjoy learning about scientific discoveries and innovations", "category": "stem", "reverse": False},
            {"id": "interest_stem_3", "text": "I like conducting experiments and testing theories", "category": "stem", "reverse": False},
            {"id": "interest_stem_4", "text": "I am interested in technology and computer systems", "category": "stem", "reverse": False},
            {"id": "interest_stem_5", "text": "I enjoy solving mathematical problems and equations", "category": "stem", "reverse": False},
            {"id": "interest_stem_6", "text": "I am curious about space, astronomy, and physics", "category": "stem", "reverse": False},
            {"id": "interest_stem_7", "text": "I like understanding how software and applications are built", "category": "stem", "reverse": False},
            {"id": "interest_stem_8", "text": "I find engineering concepts and designs interesting", "category": "stem", "reverse": False},
            
            # Arts & Humanities (8 questions)
            {"id": "interest_arts_1", "text": "I enjoy reading literature and analyzing stories", "category": "arts_humanities", "reverse": False},
            {"id": "interest_arts_2", "text": "I am interested in history and cultural studies", "category": "arts_humanities", "reverse": False},
            {"id": "interest_arts_3", "text": "I like expressing myself through writing or poetry", "category": "arts_humanities", "reverse": False},
            {"id": "interest_arts_4", "text": "I am fascinated by languages and linguistics", "category": "arts_humanities", "reverse": False},
            {"id": "interest_arts_5", "text": "I enjoy learning about philosophy and ethics", "category": "arts_humanities", "reverse": False},
            {"id": "interest_arts_6", "text": "I am interested in music, dance, or performing arts", "category": "arts_humanities", "reverse": False},
            {"id": "interest_arts_7", "text": "I like exploring different cultures and traditions", "category": "arts_humanities", "reverse": False},
            {"id": "interest_arts_8", "text": "I enjoy visual arts like painting or photography", "category": "arts_humanities", "reverse": False},
            
            # Business & Commerce (8 questions)
            {"id": "interest_business_1", "text": "I am interested in how businesses operate and grow", "category": "business_commerce", "reverse": False},
            {"id": "interest_business_2", "text": "I enjoy learning about marketing and consumer behavior", "category": "business_commerce", "reverse": False},
            {"id": "interest_business_3", "text": "I am curious about finance and investment strategies", "category": "business_commerce", "reverse": False},
            {"id": "interest_business_4", "text": "I like understanding economic trends and markets", "category": "business_commerce", "reverse": False},
            {"id": "interest_business_5", "text": "I am interested in entrepreneurship and startups", "category": "business_commerce", "reverse": False},
            {"id": "interest_business_6", "text": "I enjoy learning about management and leadership", "category": "business_commerce", "reverse": False},
            {"id": "interest_business_7", "text": "I am fascinated by accounting and financial analysis", "category": "business_commerce", "reverse": False},
            {"id": "interest_business_8", "text": "I like studying business strategies and case studies", "category": "business_commerce", "reverse": False},
            
            # Healthcare & Medicine (8 questions)
            {"id": "interest_health_1", "text": "I am interested in human anatomy and physiology", "category": "healthcare", "reverse": False},
            {"id": "interest_health_2", "text": "I enjoy learning about diseases and medical treatments", "category": "healthcare", "reverse": False},
            {"id": "interest_health_3", "text": "I am curious about nutrition and wellness", "category": "healthcare", "reverse": False},
            {"id": "interest_health_4", "text": "I like understanding how medicines and drugs work", "category": "healthcare", "reverse": False},
            {"id": "interest_health_5", "text": "I am fascinated by psychology and mental health", "category": "healthcare", "reverse": False},
            {"id": "interest_health_6", "text": "I enjoy learning about public health and epidemiology", "category": "healthcare", "reverse": False},
            {"id": "interest_health_7", "text": "I am interested in alternative medicine and therapies", "category": "healthcare", "reverse": False},
            {"id": "interest_health_8", "text": "I like studying biological sciences and life processes", "category": "healthcare", "reverse": False},
            
            # Social Service & Education (8 questions)
            {"id": "interest_social_1", "text": "I am passionate about social justice and equality", "category": "social_service", "reverse": False},
            {"id": "interest_social_2", "text": "I enjoy working with children and young people", "category": "social_service", "reverse": False},
            {"id": "interest_social_3", "text": "I am interested in community development and welfare", "category": "social_service", "reverse": False},
            {"id": "interest_social_4", "text": "I like learning about educational methods and pedagogy", "category": "social_service", "reverse": False},
            {"id": "interest_social_5", "text": "I am curious about counseling and therapeutic practices", "category": "social_service", "reverse": False},
            {"id": "interest_social_6", "text": "I enjoy volunteering and helping those in need", "category": "social_service", "reverse": False},
            {"id": "interest_social_7", "text": "I am interested in NGO work and social activism", "category": "social_service", "reverse": False},
            {"id": "interest_social_8", "text": "I like studying sociology and human behavior", "category": "social_service", "reverse": False},
        ]
    },
    
    "personality": {
        "title": "Personality Profile Assessment",
        "description": "This section evaluates key personality traits that influence your behavior, work style, and relationships.",
        "questions": [
            # Decision Making (5 questions)
            {"id": "pers_decision_1", "text": "I can make important decisions quickly even under pressure", "category": "decision_making", "reverse": False},
            {"id": "pers_decision_2", "text": "I carefully consider all options before making a choice", "category": "decision_making", "reverse": False},
            {"id": "pers_decision_3", "text": "I am comfortable making decisions with incomplete information", "category": "decision_making", "reverse": False},
            {"id": "pers_decision_4", "text": "I trust my instincts when making important choices", "category": "decision_making", "reverse": False},
            {"id": "pers_decision_5", "text": "I often second-guess my decisions after making them", "category": "decision_making", "reverse": True},
            
            # Perseverance (5 questions)
            {"id": "pers_perseverance_1", "text": "I continue working on tasks even when they become difficult", "category": "perseverance", "reverse": False},
            {"id": "pers_perseverance_2", "text": "I don't give up easily when facing obstacles", "category": "perseverance", "reverse": False},
            {"id": "pers_perseverance_3", "text": "I maintain my effort level even when progress is slow", "category": "perseverance", "reverse": False},
            {"id": "pers_perseverance_4", "text": "I finish what I start, even if it takes longer than expected", "category": "perseverance", "reverse": False},
            {"id": "pers_perseverance_5", "text": "I tend to abandon projects when they get too challenging", "category": "perseverance", "reverse": True},
            
            # Integrity (5 questions)
            {"id": "pers_integrity_1", "text": "I always choose to do the right thing even if it's difficult", "category": "integrity", "reverse": False},
            {"id": "pers_integrity_2", "text": "I am honest in my dealings with others", "category": "integrity", "reverse": False},
            {"id": "pers_integrity_3", "text": "I stand by my principles even under pressure", "category": "integrity", "reverse": False},
            {"id": "pers_integrity_4", "text": "I take responsibility for my mistakes", "category": "integrity", "reverse": False},
            {"id": "pers_integrity_5", "text": "I would compromise my values to avoid conflict", "category": "integrity", "reverse": True},
            
            # Leadership (5 questions)
            {"id": "pers_leadership_1", "text": "I naturally take charge in group situations", "category": "leadership", "reverse": False},
            {"id": "pers_leadership_2", "text": "I am comfortable delegating tasks to others", "category": "leadership", "reverse": False},
            {"id": "pers_leadership_3", "text": "I enjoy guiding and motivating team members", "category": "leadership", "reverse": False},
            {"id": "pers_leadership_4", "text": "I take initiative in organizing group activities", "category": "leadership", "reverse": False},
            {"id": "pers_leadership_5", "text": "I prefer following others rather than leading", "category": "leadership", "reverse": True},
            
            # Teamwork (5 questions)
            {"id": "pers_teamwork_1", "text": "I work well as part of a team", "category": "teamwork", "reverse": False},
            {"id": "pers_teamwork_2", "text": "I value others' input and ideas", "category": "teamwork", "reverse": False},
            {"id": "pers_teamwork_3", "text": "I am willing to compromise for the team's benefit", "category": "teamwork", "reverse": False},
            {"id": "pers_teamwork_4", "text": "I actively contribute to group discussions", "category": "teamwork", "reverse": False},
            {"id": "pers_teamwork_5", "text": "I prefer working alone rather than in groups", "category": "teamwork", "reverse": True},
            
            # Emotional Stability (5 questions)
            {"id": "pers_stability_1", "text": "I remain calm in stressful situations", "category": "emotional_stability", "reverse": False},
            {"id": "pers_stability_2", "text": "I don't let setbacks affect my mood significantly", "category": "emotional_stability", "reverse": False},
            {"id": "pers_stability_3", "text": "I handle criticism constructively", "category": "emotional_stability", "reverse": False},
            {"id": "pers_stability_4", "text": "I maintain composure under pressure", "category": "emotional_stability", "reverse": False},
            {"id": "pers_stability_5", "text": "I often feel overwhelmed by stress", "category": "emotional_stability", "reverse": True},
            
            # Risk Appetite (5 questions)
            {"id": "pers_risk_1", "text": "I am comfortable taking calculated risks", "category": "risk_appetite", "reverse": False},
            {"id": "pers_risk_2", "text": "I enjoy exploring new and uncertain opportunities", "category": "risk_appetite", "reverse": False},
            {"id": "pers_risk_3", "text": "I am willing to take chances for potential rewards", "category": "risk_appetite", "reverse": False},
            {"id": "pers_risk_4", "text": "I see change as an opportunity rather than a threat", "category": "risk_appetite", "reverse": False},
            {"id": "pers_risk_5", "text": "I prefer safe, predictable situations over uncertain ones", "category": "risk_appetite", "reverse": True},
            
            # Self-Discipline (5 questions)
            {"id": "pers_discipline_1", "text": "I can maintain focus on long-term goals", "category": "self_discipline", "reverse": False},
            {"id": "pers_discipline_2", "text": "I follow through on my commitments", "category": "self_discipline", "reverse": False},
            {"id": "pers_discipline_3", "text": "I manage my time effectively", "category": "self_discipline", "reverse": False},
            {"id": "pers_discipline_4", "text": "I can resist distractions when working", "category": "self_discipline", "reverse": False},
            {"id": "pers_discipline_5", "text": "I often procrastinate on important tasks", "category": "self_discipline", "reverse": True},
        ]
    },
    
    "aptitude": {
        "title": "Cognitive Aptitude Assessment",
        "description": "This section evaluates your cognitive abilities and problem-solving skills across various domains.",
        "questions": [
            # Verbal Reasoning (6 questions)
            {"id": "apt_verbal_1", "text": "I can easily understand and interpret written information", "category": "verbal_reasoning", "reverse": False},
            {"id": "apt_verbal_2", "text": "I am good at expressing my thoughts clearly in writing", "category": "verbal_reasoning", "reverse": False},
            {"id": "apt_verbal_3", "text": "I can quickly identify relationships between words", "category": "verbal_reasoning", "reverse": False},
            {"id": "apt_verbal_4", "text": "I enjoy analyzing and interpreting texts", "category": "verbal_reasoning", "reverse": False},
            {"id": "apt_verbal_5", "text": "I can easily summarize complex written content", "category": "verbal_reasoning", "reverse": False},
            {"id": "apt_verbal_6", "text": "I struggle with understanding written instructions", "category": "verbal_reasoning", "reverse": True},
            
            # Numerical Ability (6 questions)
            {"id": "apt_numerical_1", "text": "I am comfortable working with numbers and calculations", "category": "numerical_ability", "reverse": False},
            {"id": "apt_numerical_2", "text": "I can quickly perform mental arithmetic", "category": "numerical_ability", "reverse": False},
            {"id": "apt_numerical_3", "text": "I understand mathematical concepts easily", "category": "numerical_ability", "reverse": False},
            {"id": "apt_numerical_4", "text": "I am good at interpreting numerical data and statistics", "category": "numerical_ability", "reverse": False},
            {"id": "apt_numerical_5", "text": "I can solve mathematical problems efficiently", "category": "numerical_ability", "reverse": False},
            {"id": "apt_numerical_6", "text": "I find working with numbers confusing", "category": "numerical_ability", "reverse": True},
            
            # Logical Reasoning (6 questions)
            {"id": "apt_logical_1", "text": "I can identify patterns and sequences easily", "category": "logical_reasoning", "reverse": False},
            {"id": "apt_logical_2", "text": "I am good at drawing logical conclusions from information", "category": "logical_reasoning", "reverse": False},
            {"id": "apt_logical_3", "text": "I can solve problems using systematic thinking", "category": "logical_reasoning", "reverse": False},
            {"id": "apt_logical_4", "text": "I understand cause-and-effect relationships well", "category": "logical_reasoning", "reverse": False},
            {"id": "apt_logical_5", "text": "I can evaluate arguments and identify flaws in reasoning", "category": "logical_reasoning", "reverse": False},
            {"id": "apt_logical_6", "text": "I struggle with logical puzzles and problem-solving", "category": "logical_reasoning", "reverse": True},
            
            # Abstract Thinking (6 questions)
            {"id": "apt_abstract_1", "text": "I can easily understand abstract concepts and theories", "category": "abstract_thinking", "reverse": False},
            {"id": "apt_abstract_2", "text": "I am comfortable working with symbolic information", "category": "abstract_thinking", "reverse": False},
            {"id": "apt_abstract_3", "text": "I can identify underlying principles in complex situations", "category": "abstract_thinking", "reverse": False},
            {"id": "apt_abstract_4", "text": "I enjoy thinking about theoretical problems", "category": "abstract_thinking", "reverse": False},
            {"id": "apt_abstract_5", "text": "I can make connections between seemingly unrelated ideas", "category": "abstract_thinking", "reverse": False},
            {"id": "apt_abstract_6", "text": "I prefer concrete, practical thinking over abstract concepts", "category": "abstract_thinking", "reverse": True},
            
            # Spatial Visualization (5 questions)
            {"id": "apt_spatial_1", "text": "I can easily visualize 3D objects in my mind", "category": "spatial_visualization", "reverse": False},
            {"id": "apt_spatial_2", "text": "I am good at reading maps and understanding directions", "category": "spatial_visualization", "reverse": False},
            {"id": "apt_spatial_3", "text": "I can mentally rotate objects and shapes", "category": "spatial_visualization", "reverse": False},
            {"id": "apt_spatial_4", "text": "I understand geometric concepts easily", "category": "spatial_visualization", "reverse": False},
            {"id": "apt_spatial_5", "text": "I struggle with visualizing spatial relationships", "category": "spatial_visualization", "reverse": True},
            
            # Technological Understanding (6 questions)
            {"id": "apt_tech_1", "text": "I quickly learn how to use new technology and software", "category": "technological_understanding", "reverse": False},
            {"id": "apt_tech_2", "text": "I understand how digital systems and applications work", "category": "technological_understanding", "reverse": False},
            {"id": "apt_tech_3", "text": "I am comfortable troubleshooting technical problems", "category": "technological_understanding", "reverse": False},
            {"id": "apt_tech_4", "text": "I can easily adapt to new digital tools and platforms", "category": "technological_understanding", "reverse": False},
            {"id": "apt_tech_5", "text": "I understand basic programming and computational concepts", "category": "technological_understanding", "reverse": False},
            {"id": "apt_tech_6", "text": "I find technology confusing and difficult to understand", "category": "technological_understanding", "reverse": True},
            
            # Perceptual Speed (5 questions)
            {"id": "apt_perceptual_1", "text": "I can quickly identify differences in visual information", "category": "perceptual_speed", "reverse": False},
            {"id": "apt_perceptual_2", "text": "I notice details that others often miss", "category": "perceptual_speed", "reverse": False},
            {"id": "apt_perceptual_3", "text": "I can process visual information rapidly and accurately", "category": "perceptual_speed", "reverse": False},
            {"id": "apt_perceptual_4", "text": "I am good at spotting errors in data or documents", "category": "perceptual_speed", "reverse": False},
            {"id": "apt_perceptual_5", "text": "I often overlook important details", "category": "perceptual_speed", "reverse": True},
        ]
    },
    
    "eq": {
        "title": "Emotional Intelligence Assessment",
        "description": "This section evaluates your ability to understand, manage, and utilize emotions effectively.",
        "questions": [
            # Emotional Awareness (7 questions)
            {"id": "eq_awareness_1", "text": "I am aware of my emotions and can identify them easily", "category": "emotional_awareness", "reverse": False},
            {"id": "eq_awareness_2", "text": "I understand what triggers my emotional responses", "category": "emotional_awareness", "reverse": False},
            {"id": "eq_awareness_3", "text": "I can recognize subtle changes in my emotional state", "category": "emotional_awareness", "reverse": False},
            {"id": "eq_awareness_4", "text": "I understand the connection between my thoughts and feelings", "category": "emotional_awareness", "reverse": False},
            {"id": "eq_awareness_5", "text": "I am in touch with my inner feelings", "category": "emotional_awareness", "reverse": False},
            {"id": "eq_awareness_6", "text": "I can accurately describe my emotional experiences", "category": "emotional_awareness", "reverse": False},
            {"id": "eq_awareness_7", "text": "I often feel confused about my emotions", "category": "emotional_awareness", "reverse": True},
            
            # Emotional Regulation (7 questions)
            {"id": "eq_regulation_1", "text": "I can control my emotional reactions in difficult situations", "category": "emotional_regulation", "reverse": False},
            {"id": "eq_regulation_2", "text": "I manage stress effectively", "category": "emotional_regulation", "reverse": False},
            {"id": "eq_regulation_3", "text": "I can calm myself when upset or angry", "category": "emotional_regulation", "reverse": False},
            {"id": "eq_regulation_4", "text": "I don't let negative emotions affect my performance", "category": "emotional_regulation", "reverse": False},
            {"id": "eq_regulation_5", "text": "I can delay gratification when necessary", "category": "emotional_regulation", "reverse": False},
            {"id": "eq_regulation_6", "text": "I bounce back quickly from emotional setbacks", "category": "emotional_regulation", "reverse": False},
            {"id": "eq_regulation_7", "text": "I often react impulsively when emotionally charged", "category": "emotional_regulation", "reverse": True},
            
            # Empathy (7 questions)
            {"id": "eq_empathy_1", "text": "I can easily understand how others are feeling", "category": "empathy", "reverse": False},
            {"id": "eq_empathy_2", "text": "I am sensitive to other people's emotions", "category": "empathy", "reverse": False},
            {"id": "eq_empathy_3", "text": "I can see situations from others' perspectives", "category": "empathy", "reverse": False},
            {"id": "eq_empathy_4", "text": "I genuinely care about others' well-being", "category": "empathy", "reverse": False},
            {"id": "eq_empathy_5", "text": "I can pick up on unspoken emotional cues", "category": "empathy", "reverse": False},
            {"id": "eq_empathy_6", "text": "I respond compassionately to others' distress", "category": "empathy", "reverse": False},
            {"id": "eq_empathy_7", "text": "I find it difficult to understand others' feelings", "category": "empathy", "reverse": True},
            
            # Social Skills (7 questions)
            {"id": "eq_social_1", "text": "I build rapport easily with new people", "category": "social_skills", "reverse": False},
            {"id": "eq_social_2", "text": "I communicate effectively in social situations", "category": "social_skills", "reverse": False},
            {"id": "eq_social_3", "text": "I can influence and persuade others positively", "category": "social_skills", "reverse": False},
            {"id": "eq_social_4", "text": "I work well in diverse groups", "category": "social_skills", "reverse": False},
            {"id": "eq_social_5", "text": "I can resolve conflicts constructively", "category": "social_skills", "reverse": False},
            {"id": "eq_social_6", "text": "I maintain positive relationships with others", "category": "social_skills", "reverse": False},
            {"id": "eq_social_7", "text": "I struggle in social interactions", "category": "social_skills", "reverse": True},
            
            # Motivation (6 questions)
            {"id": "eq_motivation_1", "text": "I stay motivated even when facing setbacks", "category": "motivation", "reverse": False},
            {"id": "eq_motivation_2", "text": "I am driven to achieve my goals", "category": "motivation", "reverse": False},
            {"id": "eq_motivation_3", "text": "I maintain enthusiasm for long-term projects", "category": "motivation", "reverse": False},
            {"id": "eq_motivation_4", "text": "I find intrinsic satisfaction in my work", "category": "motivation", "reverse": False},
            {"id": "eq_motivation_5", "text": "I persist despite obstacles", "category": "motivation", "reverse": False},
            {"id": "eq_motivation_6", "text": "I lose interest in goals quickly", "category": "motivation", "reverse": True},
            
            # Conflict Management (6 questions)
            {"id": "eq_conflict_1", "text": "I handle conflicts calmly and constructively", "category": "conflict_management", "reverse": False},
            {"id": "eq_conflict_2", "text": "I can mediate disagreements between others", "category": "conflict_management", "reverse": False},
            {"id": "eq_conflict_3", "text": "I address conflicts directly rather than avoiding them", "category": "conflict_management", "reverse": False},
            {"id": "eq_conflict_4", "text": "I seek win-win solutions in disputes", "category": "conflict_management", "reverse": False},
            {"id": "eq_conflict_5", "text": "I remain objective during disagreements", "category": "conflict_management", "reverse": False},
            {"id": "eq_conflict_6", "text": "I become defensive when challenged", "category": "conflict_management", "reverse": True},
        ]
    }
}

def get_questions_by_type(test_type):
    """Get all questions for a specific test type"""
    if test_type not in QUESTION_BANK:
        return None
    
    test_data = QUESTION_BANK[test_type]
    questions = []
    
    for q in test_data["questions"]:
        questions.append({
            "id": q["id"],
            "question": q["text"],
            "type": "scale",
            "category": q.get("category", ""),
            "reverse": q.get("reverse", False)
        })
    
    return {
        "test_type": test_type,
        "title": test_data["title"],
        "description": test_data["description"],
        "questions": questions,
        "total_questions": len(questions)
    }

def get_all_question_counts():
    """Get count of questions for each test type"""
    counts = {}
    total = 0
    for test_type, data in QUESTION_BANK.items():
        count = len(data["questions"])
        counts[test_type] = count
        total += count
    counts["total"] = total
    return counts

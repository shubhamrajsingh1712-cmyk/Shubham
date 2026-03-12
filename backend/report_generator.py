"""
Comprehensive PDF Report Generator for BoatMyCareer.com
Generates 18-20 page detailed psychometric assessment reports
Inspired by Mindler-style detailed trait analysis
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, Image as RLImage, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime
from typing import Dict, List, Any
import numpy as np

# ============================================================
# TRAIT INTERPRETATION DATA
# For each trait: meaning, and analysis/plan per band (High/Moderate/Low)
# ============================================================
TRAIT_DATA = {
    # --- ORIENTATION ---
    "creative": {
        "label": "Creative",
        "meaning": "Creative orientation measures your natural inclination towards imaginative thinking, innovation, and artistic expression. Individuals with a strong creative orientation tend to seek novel solutions, enjoy brainstorming, and feel energized by open-ended tasks that allow them to think outside the box.",
        "High": {
            "analysis": "Your score indicates a strong creative orientation. You are naturally drawn to innovative problem-solving and original thinking. You likely enjoy brainstorming sessions, artistic pursuits, and tasks that require imagination. You may find routine work unstimulating and instead thrive when given the freedom to experiment and explore new ideas. Your creative mindset is a valuable asset in today's innovation-driven economy.",
            "plan": ["Seek internships or projects in design, media, content creation, or creative technology to channel your creativity productively.|Explore creative outlets such as writing, art, music, or digital design to further develop your creative thinking skills.|Practice structured brainstorming techniques like mind-mapping and SCAMPER to make your creativity more focused and productive.|Consider careers that blend creativity with other skills, such as UX Design, Architecture, Advertising, or Product Development."]
        },
        "Moderate": {
            "analysis": "Your score indicates a balanced creative orientation. You appreciate creative thinking and can generate innovative ideas when needed, but you also value structure and practicality. This balance allows you to be adaptable across different work settings. You can contribute creative solutions while also being comfortable with routine tasks when required.",
            "plan": ["Challenge yourself with creative projects outside your comfort zone to develop this area further.|Take up a creative hobby such as photography, blogging, or sketching to exercise your imagination regularly.|Practice 'thinking differently' by approaching everyday problems from multiple angles before settling on a solution.|Explore careers that balance creativity with analytical work, such as Marketing Analytics, Product Management, or Science Communication."]
        },
        "Low": {
            "analysis": "Your score suggests that you prefer structured, well-defined tasks over open-ended creative work. This does not mean you lack creativity — rather, you may feel more comfortable when there are clear guidelines and procedures to follow. You likely prefer roles with defined processes and measurable outcomes. Your strength lies in executing plans systematically and reliably.",
            "plan": ["Try small creative exercises like journaling or doodling to gradually build comfort with open-ended thinking.|Participate in group brainstorming sessions where you can contribute your structured thinking to complement others' creative ideas.|Look for roles that value systematic execution such as Quality Assurance, Operations, Accounting, or Data Entry.|Remember that creativity is a skill that can be developed — start with small, low-pressure creative tasks and build from there."]
        }
    },
    "analytical": {
        "label": "Analytical",
        "meaning": "Analytical orientation measures your preference for logical reasoning, data-driven decision making, and systematic problem-solving. People with a strong analytical orientation enjoy breaking down complex problems into components, finding patterns in data, and making evidence-based conclusions.",
        "High": {
            "analysis": "Your high analytical score reveals a natural ability for systematic thinking and data-driven problem solving. You likely enjoy dissecting complex problems, finding patterns, and reaching logical conclusions. Your mind gravitates towards evidence-based approaches, and you feel most confident when decisions are backed by facts and thorough analysis. This is a highly valued trait in today's data-centric world.",
            "plan": ["Develop your data analysis skills through tools like Excel, Python, or R to complement your analytical mindset.|Participate in science fairs, math olympiads, or coding competitions to sharpen your analytical abilities.|Consider careers in Data Science, Engineering, Research, Finance, or Consulting that heavily rely on analytical skills.|Practice communicating your analyses clearly to others, as strong analytical thinking paired with communication skills is extremely powerful."]
        },
        "Moderate": {
            "analysis": "Your analytical orientation is at a balanced level. You can apply logical thinking when needed and are comfortable working with data and structured problems. However, you also rely on intuition and experience alongside pure analysis. This balance makes you adaptable — you can work in both analytical and people-oriented environments effectively.",
            "plan": ["Strengthen your analytical skills by taking online courses in logic, statistics, or critical thinking.|Practice analyzing real-world situations like business case studies or scientific articles to build your analytical confidence.|Explore careers that blend analytical thinking with interpersonal skills, such as Business Analysis, Healthcare Management, or Teaching.|Use analytical frameworks like SWOT analysis or pros-and-cons lists to make important decisions in your daily life."]
        },
        "Low": {
            "analysis": "Your score suggests you prefer intuitive, experience-based approaches over purely analytical methods. You may find extensive data analysis tedious and prefer to make decisions based on gut feeling, personal experience, or emotional intelligence. This is not a weakness — many successful leaders rely on intuition and emotional intelligence rather than pure analysis.",
            "plan": ["Build basic analytical skills through short courses in Excel or basic statistics to ensure you can handle data when needed.|Practice breaking down decisions into pros and cons to add a layer of analysis to your intuitive approach.|Seek roles that value relationship-building, creativity, or hands-on work over heavy data analysis.|Partner with analytically-minded peers on projects to create complementary strengths in team settings."]
        }
    },
    "people_centric": {
        "label": "People Centric",
        "meaning": "People-centric orientation measures your natural inclination towards working with and for people. It reflects your preference for collaboration, teamwork, communication, and interpersonal engagement. Individuals with a strong people orientation find energy in social interactions and derive satisfaction from helping others.",
        "High": {
            "analysis": "Your high people-centric score indicates a strong natural orientation towards working with others. You thrive in collaborative environments, enjoy building relationships, and find genuine satisfaction in helping people. You are likely an effective communicator who can build rapport quickly. Your empathetic nature and social awareness make you well-suited for roles that involve client interaction, team leadership, or community service.",
            "plan": ["Develop your leadership skills through student council, volunteer work, or community organizing activities.|Practice active listening and conflict resolution skills to strengthen your interpersonal effectiveness.|Consider careers in Teaching, Counseling, Human Resources, Healthcare, Social Work, or Sales where people skills are essential.|Explore public speaking or debate to refine your communication abilities and build confidence in group settings."]
        },
        "Moderate": {
            "analysis": "Your people-centric orientation is at a moderate level, indicating a healthy balance between social engagement and independent work. You are comfortable working in teams but also value your personal space and independent work time. You can collaborate effectively when needed but do not feel drained by working alone. This flexibility is advantageous across many career paths.",
            "plan": ["Strengthen your networking skills by attending workshops or social events to build your professional connections.|Practice both collaborative and independent working styles to maintain your versatility.|Look for careers that offer a mix of teamwork and independent tasks, such as Project Management, Research, or Marketing.|Volunteer for team-based activities to expand your comfort zone in social settings while maintaining your independence."]
        },
        "Low": {
            "analysis": "Your score suggests a preference for independent work over team-based activities. You may feel most productive when working alone and find prolonged social interaction draining. This is perfectly valid — many impactful careers reward deep, focused individual work. You likely prefer communicating through written means rather than extensive face-to-face interaction, and you value autonomy in your work.",
            "plan": ["Practice small-group interactions to gradually build your comfort with collaboration when needed.|Develop written communication skills as they will be your primary mode of professional interaction.|Consider careers that value independent expertise such as Software Development, Writing, Research, Accounting, or Data Analysis.|When working in teams, take on roles that allow focused individual contributions, such as the researcher or the specialist."]
        }
    },
    "administrative": {
        "label": "Administrative",
        "meaning": "Administrative orientation measures your natural preference for organization, planning, structured processes, and systematic execution. People with strong administrative orientation excel at managing details, following procedures, maintaining records, and ensuring operational efficiency.",
        "High": {
            "analysis": "Your high administrative score reflects a strong natural ability for organization, planning, and systematic execution. You feel most comfortable when there are clear processes, defined roles, and structured workflows. You are likely very detail-oriented, reliable, and consistent in your work. Your ability to maintain order and manage complex administrative tasks is a valuable asset in any organization.",
            "plan": ["Develop project management skills through tools like Trello, Asana, or Microsoft Project to formalize your organizational abilities.|Consider pursuing certifications in management or operations to complement your administrative strengths.|Explore careers in Operations Management, Administration, Government Services, Banking, or Quality Assurance.|Practice delegation and strategic thinking to evolve from task management to leadership and strategic planning."]
        },
        "Moderate": {
            "analysis": "Your moderate administrative score indicates a balanced approach to organization and planning. You appreciate structure but are also comfortable with some flexibility and ambiguity. You can manage administrative tasks effectively but may also enjoy more creative or people-oriented work. This adaptability allows you to function well across different types of roles and environments.",
            "plan": ["Develop basic organizational tools and habits (calendars, to-do lists, filing systems) to strengthen your administrative efficiency.|Learn time management techniques like the Pomodoro method or Eisenhower matrix to enhance productivity.|Look for roles that combine organizational skills with your other strengths, such as Event Management, Healthcare Administration, or Teaching.|Practice planning skills by organizing school events, study groups, or community projects."]
        },
        "Low": {
            "analysis": "Your score indicates that you prefer flexibility and spontaneity over rigid planning and structure. Routine administrative tasks may feel restrictive to you. You likely prefer environments that allow adaptation, creativity, and freedom from excessive bureaucracy. While this can fuel innovation, developing some organizational skills will help you manage the practical aspects of any career.",
            "plan": ["Start with simple organizational habits like maintaining a daily planner or setting reminders for deadlines.|Use digital tools like Google Calendar or Notion to build minimal but effective organizational systems.|Seek careers that offer flexibility and variety rather than rigid administrative structures, such as Journalism, Consulting, Creative Arts, or Entrepreneurship.|Partner with organized peers on projects where administrative management is critical to balance your spontaneous approach."]
        }
    },
    # --- INTEREST ---
    "stem": {
        "label": "STEM (Science, Technology, Engineering, Mathematics)",
        "meaning": "This measures your interest in scientific inquiry, technological innovation, engineering problem-solving, and mathematical reasoning. A strong STEM interest indicates enthusiasm for understanding how things work, building solutions, and working with numbers and logical systems.",
        "High": {
            "analysis": "Your high STEM interest reveals a strong passion for science and technology. You enjoy understanding how things work, solving technical problems, and working with numbers and logic. You likely find science experiments, coding, or mathematical puzzles stimulating. This interest, combined with the right aptitude, can open doors to some of the most rewarding and impactful careers in today's economy.",
            "plan": ["Participate in science olympiads, coding competitions, or maker fairs to deepen your STEM engagement.|Start learning a programming language (Python, Java) or exploring STEM projects through platforms like Arduino or Raspberry Pi.|Consider career paths like Software Engineering, Data Science, Medicine, Biotechnology, or Aerospace Engineering.|Seek mentors in STEM fields and explore internship opportunities in labs, tech companies, or engineering firms."]
        },
        "Moderate": {
            "analysis": "Your moderate STEM interest indicates a balanced appreciation for science and technology. While you find STEM subjects interesting, they may not be your primary passion. You can engage with technical topics effectively but also enjoy other domains equally. This balanced interest can lead to interdisciplinary careers that blend STEM with other fields.",
            "plan": ["Explore the intersection of STEM with your other interests, such as Science Communication, Healthcare Management, or EdTech.|Take introductory courses in coding or data analysis to build foundational STEM skills that complement any career.|Consider careers like Medical Illustration, Environmental Policy, Science Journalism, or Business Analytics.|Stay curious about technological developments even if STEM isn't your primary focus — technology literacy is valuable in every field."]
        },
        "Low": {
            "analysis": "Your responses suggest that STEM subjects are not your primary area of interest. You may find pure scientific or mathematical work less engaging compared to creative, social, or business-oriented activities. This is perfectly fine — many fulfilling careers do not require deep STEM engagement. Your strengths likely lie in areas that value communication, creativity, or interpersonal skills.",
            "plan": ["Maintain basic technology literacy through simple tools and digital skills that are essential in modern workplaces.|Explore careers in Arts, Humanities, Business, Law, Social Work, or Media that align better with your interests.|If you need to engage with STEM for academic purposes, try finding real-world applications that make the topics more interesting.|Remember that every career path has value — your strengths in non-STEM areas are equally important and in demand."]
        }
    },
    "arts_humanities": {
        "label": "Arts & Humanities",
        "meaning": "This measures your interest in creative expression, culture, literature, languages, history, philosophy, and human experiences. A strong interest here indicates a passion for understanding human behavior, expressing ideas through art or writing, and engaging with cultural and social topics.",
        "High": {
            "analysis": "Your high score in Arts and Humanities reveals a deep appreciation for creative expression, culture, and the human experience. You likely enjoy reading, writing, artistic pursuits, or engaging with philosophical and social questions. You find meaning in stories, ideas, and cultural exploration. This passion can lead to deeply fulfilling careers that shape culture and communicate ideas.",
            "plan": ["Develop a portfolio of creative work (writing, art, photography, design) to showcase your talents.|Participate in literary competitions, art exhibitions, drama clubs, or debate societies to hone your skills.|Explore careers in Journalism, Content Creation, Film, Fine Arts, Architecture, Interior Design, or Publishing.|Consider how your creative interests can combine with technology (UX Design, Game Design, Digital Media) for broader career options."]
        },
        "Moderate": {
            "analysis": "Your moderate Arts and Humanities interest shows a balanced appreciation for creative and cultural topics alongside other areas. You enjoy creative expression but may not see it as your primary career driver. This balance allows you to bring a creative perspective to non-artistic fields, making you versatile in many professional environments.",
            "plan": ["Keep your creative skills active through hobbies like writing, reading, or attending cultural events.|Use your creative perspective as a differentiator in your chosen field — creativity is valued in every profession.|Explore interdisciplinary careers like Advertising, Brand Management, Science Communication, or Education that blend creativity with other domains.|Take a creative writing or design course to develop your artistic skills even if your primary career path lies elsewhere."]
        },
        "Low": {
            "analysis": "Your responses indicate that Arts and Humanities are not your primary area of interest. You may prefer practical, technical, or data-driven activities over creative or philosophical pursuits. While artistic expression may not be your focus, maintaining some engagement with the arts can enhance your overall personal development and communication skills.",
            "plan": ["Try consuming art and culture casually (films, podcasts, museums) to build cultural awareness without pressure.|Focus on your stronger interest areas where you will find more natural motivation and career satisfaction.|Develop basic communication and presentation skills, which draw on humanities-related competencies and are essential in every career.|Explore how your preferred fields (STEM, Business) incorporate creative elements to find a natural connection to the arts."]
        }
    },
    "business_commerce": {
        "label": "Business & Commerce",
        "meaning": "This measures your interest in business operations, finance, marketing, entrepreneurship, and commercial activities. A strong business interest indicates enthusiasm for understanding markets, managing money, creating ventures, and driving economic outcomes.",
        "High": {
            "analysis": "Your high Business and Commerce interest indicates a strong attraction to the world of finance, entrepreneurship, and business operations. You likely enjoy understanding how businesses work, analyzing market trends, and thinking about commercial strategies. You may already have entrepreneurial ideas or a natural interest in investing, trading, or running a venture.",
            "plan": ["Start a small business or participate in entrepreneurship competitions to gain real-world business experience.|Learn fundamentals of accounting, marketing, and finance through online courses or school subjects.|Explore career paths like Chartered Accountancy, Investment Banking, Marketing Management, Entrepreneurship, or Consulting.|Read business publications (Economic Times, Harvard Business Review) and follow successful entrepreneurs for inspiration."]
        },
        "Moderate": {
            "analysis": "Your moderate Business and Commerce interest shows a balanced appreciation for commercial activities. You understand the importance of business skills but may not see them as your primary passion. This practical awareness of business concepts will serve you well regardless of your chosen career field, as business acumen is valuable in every profession.",
            "plan": ["Build basic financial literacy skills including budgeting, investing fundamentals, and understanding financial statements.|Explore careers that blend business with your primary interests, such as Healthcare Management, Sports Management, or Art Direction.|Consider taking a business elective or joining a commerce-related club to expand your commercial understanding.|Learn basic marketing and communication skills that will be useful regardless of your ultimate career choice."]
        },
        "Low": {
            "analysis": "Your responses suggest that business and commercial activities are not your primary interest. You may prefer creative, scientific, or service-oriented pursuits over financial and market-driven work. While business may not excite you directly, basic financial literacy and commercial awareness are important life skills that will benefit you in any career path.",
            "plan": ["Learn basic personal finance skills (budgeting, saving, investing) even if business is not your career focus.|Focus on your stronger interest areas where you will find more passion and career satisfaction.|Consider how your preferred field generates income and creates value — this business awareness will make you more effective.|Explore how non-business careers like Medicine, Arts, or Social Work have business aspects that require some commercial understanding."]
        }
    },
    "healthcare": {
        "label": "Healthcare & Medical Sciences",
        "meaning": "This measures your interest in medical sciences, patient care, health promotion, and biomedical research. A strong healthcare interest indicates enthusiasm for understanding the human body, helping people recover from illness, and contributing to public health and wellness.",
        "High": {
            "analysis": "Your high Healthcare interest reveals a strong passion for medical sciences and helping people with their health. You likely find biology and human anatomy fascinating, and you feel motivated by the idea of healing and caring for others. This compassionate drive, combined with scientific curiosity, is the foundation of many rewarding healthcare careers.",
            "plan": ["Volunteer at hospitals, clinics, or old-age homes to gain firsthand experience with healthcare settings.|Focus on strengthening your biology, chemistry, and physics knowledge as these form the foundation of medical education.|Explore diverse healthcare career paths: Medicine (MBBS), Dentistry, Pharmacy, Physiotherapy, Psychology, Nursing, or Public Health.|Prepare early for entrance exams like NEET if you are seriously considering a medical career path."]
        },
        "Moderate": {
            "analysis": "Your moderate Healthcare interest indicates a balanced appreciation for medical sciences. While healthcare topics interest you, they may not be your sole passion. This awareness of health and wellness can complement other career choices and opens doors to interdisciplinary fields that bridge healthcare with other domains.",
            "plan": ["Explore healthcare-adjacent careers like Health Communication, Medical Technology, Healthcare Administration, or Biomedical Engineering.|Maintain your interest in health sciences through casual learning (documentaries, health blogs, first aid courses).|Consider how healthcare intersects with your primary interest areas for unique career combinations.|Develop empathy and caring skills that will be valuable regardless of whether you enter healthcare directly."]
        },
        "Low": {
            "analysis": "Your responses suggest that healthcare and medical sciences are not your primary area of interest. You may find other domains more engaging and motivating. This is perfectly normal — there are many impactful career paths outside healthcare. Focus on areas where your natural interests and strengths converge for the best career outcomes.",
            "plan": ["Maintain basic health literacy and first aid knowledge as essential life skills.|Focus on your areas of stronger interest where you will find more passion and engagement.|Explore how your preferred career field contributes to health and wellbeing indirectly (technology in health, environmental health, etc.).|If you need to study biology or health sciences academically, try finding connections to your primary interests to maintain motivation."]
        }
    },
    "social_service": {
        "label": "Social Service & Community Work",
        "meaning": "This measures your interest in community development, social welfare, education, helping the underprivileged, and creating positive social impact. A strong social service interest indicates a desire to serve others, fight inequality, and contribute to building a better society.",
        "High": {
            "analysis": "Your high Social Service interest reveals a strong desire to make a positive impact on society. You are likely motivated by helping others, fighting for justice, and contributing to community welfare. You find meaning in work that serves the greater good and may already be involved in volunteer activities or social causes. This compassion-driven motivation is the hallmark of changemakers.",
            "plan": ["Get actively involved in community service, NGO volunteer work, or social entrepreneurship projects.|Develop skills in communication, project management, and fundraising that are essential for social sector careers.|Explore careers in Social Work, Teaching, Non-Profit Management, Public Policy, Development Studies, or Community Health.|Consider how social impact can be combined with other fields like Law (Human Rights), Technology (Social Tech), or Business (Social Enterprise)."]
        },
        "Moderate": {
            "analysis": "Your moderate Social Service interest shows a balanced awareness of social issues and community needs. While helping others matters to you, it may not be your sole career driver. This sensitivity to social impact will enhance any career you choose, as most organizations value socially conscious employees who care about making a positive difference.",
            "plan": ["Volunteer occasionally for causes you care about to maintain your connection to social service.|Explore how your primary career interest can create social impact — every profession has opportunities for community contribution.|Consider Corporate Social Responsibility (CSR) roles that blend business careers with social impact.|Develop your empathy and communication skills, which are valuable in every professional context."]
        },
        "Low": {
            "analysis": "Your responses indicate that social service work is not your primary area of interest. You may prefer individual achievement, technical challenges, or creative pursuits over community-oriented work. While direct social service may not appeal to you, understanding social dynamics and developing empathy are important for personal growth and professional success.",
            "plan": ["Participate in at least one community activity per year to maintain a connection with social issues.|Focus on your areas of stronger interest where you will find natural motivation and satisfaction.|Explore how your chosen career contributes to society indirectly — all meaningful work creates some social value.|Develop basic empathy and social awareness skills that will help in any interpersonal professional setting."]
        }
    },
    # --- PERSONALITY ---
    "decision_making": {
        "label": "Decision Making",
        "meaning": "Decision making measures your ability to evaluate options, weigh consequences, and make informed choices confidently. Strong decision makers analyze situations quickly, consider multiple perspectives, and commit to a course of action without excessive hesitation or regret.",
        "High": {
            "analysis": "Your strong decision-making score indicates you are confident in evaluating options and making choices. You tend to analyze situations effectively, weigh pros and cons, and commit to your decisions without excessive second-guessing. This decisiveness is highly valued in leadership and management roles, where timely and confident decisions can make a significant impact.",
            "plan": ["Practice making decisions in increasingly complex scenarios (group projects, competitions, debates).|Learn formal decision-making frameworks like Decision Trees and Cost-Benefit Analysis to add rigor to your natural decisiveness.|Consider leadership-oriented careers in Management, Entrepreneurship, Consulting, or Military Services.|Be mindful of potential overconfidence — seek diverse perspectives before making critical decisions."]
        },
        "Moderate": {
            "analysis": "Your moderate decision-making score suggests a balanced approach — you can make decisions effectively but may sometimes hesitate when facing complex or high-stakes situations. You likely prefer to gather sufficient information before committing, which is a thoughtful approach. Building confidence in your decisions will strengthen your overall effectiveness.",
            "plan": ["Practice making small decisions quickly to build your decision-making confidence gradually.|Keep a decision journal — record your decisions and outcomes to learn from your patterns.|Explore time-boxing techniques — give yourself a deadline for decisions to avoid overthinking.|Seek mentors who can guide you through complex decision-making processes to build your confidence."]
        },
        "Low": {
            "analysis": "Your score suggests that decision-making can be challenging for you. You may experience difficulty committing to choices, especially when there are many options or high stakes involved. This may stem from a desire to make the perfect decision, which can lead to overthinking or indecisiveness. Building a structured approach to decisions can help you overcome this challenge.",
            "plan": ["Start with small decisions and practice committing to them without revisiting — build your decision-making muscle.|Use the 70% rule — if you have 70% of the information you need, make the decision and adjust later if needed.|Practice pros-and-cons lists for important decisions to create a structured framework for choosing.|Consider seeking a trusted advisor (parent, teacher, mentor) who can help you talk through major decisions."]
        }
    },
    "perseverance": {
        "label": "Perseverance",
        "meaning": "Perseverance measures your ability to persist through challenges, setbacks, and long-term goals without giving up. It reflects your grit, determination, and capacity to maintain effort even when results are not immediately visible or when obstacles seem overwhelming.",
        "High": {
            "analysis": "Your high perseverance score is an outstanding strength. You demonstrate remarkable determination and grit — when you commit to a goal, you see it through despite obstacles and setbacks. You likely don't give up easily and view challenges as opportunities to grow. This trait is one of the strongest predictors of long-term success in any field.",
            "plan": ["Channel your perseverance into long-term goals like competitive exam preparation, skill mastery, or project completion.|Share your determination with peers — your grit can inspire and motivate others in group projects.|Consider demanding careers like Medicine, Civil Services, Research, or Competitive Sports that reward sustained effort.|Ensure you balance perseverance with self-care — know when to push through and when to rest and recover."]
        },
        "Moderate": {
            "analysis": "Your moderate perseverance score indicates a balanced approach to persistence. You can push through challenges when sufficiently motivated but may struggle with tasks that don't interest you or seem unrewarding. Building consistent perseverance habits will significantly enhance your ability to achieve long-term goals in your chosen career.",
            "plan": ["Set smaller milestones within large goals to maintain motivation and track your progress.|Practice the 'just five more minutes' technique — when you feel like quitting, push through for just a bit longer.|Find your personal motivation triggers — understanding what drives you will help sustain effort during tough times.|Join study groups or accountability partners who can help you stay committed to your goals."]
        },
        "Low": {
            "analysis": "Your score suggests that maintaining long-term effort through challenges can be difficult. You may find it hard to stay motivated when results are slow or when obstacles arise. This is an important area for development, as perseverance is a critical factor in academic and career success. The good news is that grit can be built through practice.",
            "plan": ["Start with small, achievable goals and celebrate each completion to build your confidence in persisting.|Break large tasks into tiny steps — focusing on the next small action is less overwhelming than the entire goal.|Find a passion or purpose that naturally motivates you — perseverance is easier when you deeply care about the outcome.|Practice delayed gratification through small exercises like saving for something you want instead of buying immediately."]
        }
    },
    "integrity": {
        "label": "Integrity",
        "meaning": "Integrity measures your commitment to honesty, ethical behavior, moral values, and principled conduct. Individuals with strong integrity are consistent in their values, transparent in their actions, and trustworthy in their relationships, even when no one is watching.",
        "High": {
            "analysis": "Your high integrity score is commendable. You demonstrate a strong commitment to honesty, ethical behavior, and moral values. People likely trust you and see you as reliable and principled. You value fairness and are uncomfortable with dishonesty or unethical shortcuts. This character strength is the foundation of meaningful relationships and a respected career.",
            "plan": ["Continue to uphold your values while learning to navigate ethical dilemmas that may arise in professional settings.|Consider careers where integrity is paramount: Law, Medicine, Civil Services, Teaching, Auditing, or Judiciary.|Develop your ability to stand firm on ethical issues while being diplomatic in expressing disagreement.|Read about ethical leadership and real-world case studies to prepare for complex moral situations you may face."]
        },
        "Moderate": {
            "analysis": "Your moderate integrity score indicates that you generally value honesty and ethical behavior but may sometimes face situations where your principles are tested. You have a good moral compass but may benefit from strengthening your resolve in difficult ethical situations. Building a stronger ethical framework will enhance your trustworthiness and professional reputation.",
            "plan": ["Reflect on your core values and write them down — having clarity about what you stand for helps in ethical decision-making.|Practice saying 'no' to small ethical compromises to build your integrity muscle for bigger situations.|Read about ethical dilemmas in your areas of interest to prepare yourself for complex real-world scenarios.|Seek role models who demonstrate strong integrity and learn from their approach to difficult situations."]
        },
        "Low": {
            "analysis": "Your score suggests that ethical considerations may not always be at the forefront of your decision-making. This could indicate a pragmatic approach that sometimes prioritizes outcomes over principles. Developing stronger ethical awareness is important for building trust, maintaining professional relationships, and ensuring long-term career success.",
            "plan": ["Begin developing a personal code of ethics — identify non-negotiable values that you will always uphold.|Practice transparency in your daily interactions to build trust with peers, teachers, and family.|Study the consequences of ethical failures in businesses and careers to understand why integrity matters for long-term success.|Seek guidance from a mentor or counselor who can help you develop stronger ethical reasoning skills."]
        }
    },
    "leadership": {
        "label": "Leadership",
        "meaning": "Leadership measures your natural ability and desire to guide, influence, and inspire others towards common goals. It reflects your comfort with taking charge, making decisions for a group, and assuming responsibility for outcomes.",
        "High": {
            "analysis": "Your high leadership score reveals a natural ability to take charge and inspire others. You are likely comfortable making decisions for a group, delegating tasks, and motivating team members. People may naturally look to you for guidance in group settings. Your leadership potential, if nurtured with the right skills and experience, can make you highly effective in management and executive roles.",
            "plan": ["Take on leadership roles in school clubs, student council, sports teams, or community organizations to develop your skills.|Learn different leadership styles (democratic, transformational, servant leadership) to become a versatile leader.|Practice active listening and empathy alongside your natural authority to become a more balanced leader.|Consider careers with significant leadership opportunities: Management, Military, Politics, Entrepreneurship, or Education Administration."]
        },
        "Moderate": {
            "analysis": "Your moderate leadership score indicates that you can lead when necessary but may not actively seek leadership positions. You are comfortable contributing as both a leader and a team member, which is a versatile quality. Developing your leadership confidence will expand your career options and make you more effective in collaborative environments.",
            "plan": ["Start leading small projects or study groups to build your leadership confidence gradually.|Learn from leaders you admire — observe their communication style, decision-making approach, and team management.|Practice public speaking to develop the communication skills essential for effective leadership.|Explore leadership development programs or workshops that can help you build structured leadership abilities."]
        },
        "Low": {
            "analysis": "Your score suggests that leadership roles may not come naturally to you. You may prefer to contribute as a team member rather than taking charge. This does not mean you cannot lead — it means you may need more practice and confidence-building in leadership situations. Many successful professionals are excellent individual contributors who lead through expertise rather than authority.",
            "plan": ["Start with informal leadership opportunities like helping a friend with a project or mentoring a younger student.|Develop your subject matter expertise — 'thought leadership' through deep knowledge can be as powerful as formal leadership.|Practice voicing your opinions in group settings to build confidence in influencing others.|Explore careers that value deep expertise and individual contribution, such as Research, Writing, Specialist Consulting, or Technical Roles."]
        }
    },
    "teamwork": {
        "label": "Teamwork",
        "meaning": "Teamwork measures your ability and preference for working collaboratively with others towards shared goals. It reflects your skill in cooperating, compromising, communicating within groups, and contributing to collective success.",
        "High": {
            "analysis": "Your high teamwork score reveals a strong collaborative nature. You work well with others, contribute positively to group dynamics, and value collective success. You are likely an effective communicator in group settings and can navigate interpersonal dynamics smoothly. This is an essential skill in today's interconnected workplace where most significant achievements require team effort.",
            "plan": ["Take on collaborative project roles to further develop your teamwork skills across diverse group settings.|Learn conflict resolution and negotiation skills to handle team disagreements constructively.|Explore careers that thrive on collaboration: Project Management, Consulting, Healthcare, Event Management, or Team Sports.|Practice leading teams occasionally to add leadership skills to your strong collaborative foundation."]
        },
        "Moderate": {
            "analysis": "Your moderate teamwork score indicates a balanced approach to collaboration. You can work effectively in teams but also value independent work time. You may prefer smaller, focused teams over large collaborative groups. This balance is valuable — you can contribute to teams while also delivering strong individual work.",
            "plan": ["Practice collaborative skills in diverse team settings to expand your comfort with different group dynamics.|Communicate your work style preferences clearly to team members — this helps set expectations and reduces friction.|Develop both collaborative and independent working strategies to maximize your versatility.|Explore roles that offer a balanced mix of teamwork and individual responsibility."]
        },
        "Low": {
            "analysis": "Your score suggests a preference for independent work over team-based collaboration. You may find group dynamics challenging or feel that your best work happens when you can focus alone. While independent capability is valuable, most careers require some degree of teamwork, so developing collaborative skills will enhance your professional effectiveness.",
            "plan": ["Start participating in small group activities (2-3 people) to build comfort with collaboration gradually.|Practice communication skills that facilitate teamwork — clear expression, active listening, and constructive feedback.|Seek roles that primarily involve independent work but occasionally require team interaction, such as Research, Writing, or Programming.|Remember that teamwork is a skill, not a personality trait — with practice, you can become more comfortable and effective in team settings."]
        }
    },
    "emotional_stability": {
        "label": "Emotional Stability",
        "meaning": "Emotional stability measures your ability to remain calm, composed, and balanced under pressure or during stressful situations. It reflects your capacity to manage emotions effectively, cope with setbacks, and maintain psychological equilibrium.",
        "High": {
            "analysis": "Your high emotional stability score indicates excellent emotional regulation. You tend to remain calm under pressure, handle stress effectively, and recover quickly from setbacks. People likely see you as composed and reliable, even in challenging situations. This stability is a significant asset in high-pressure careers and leadership roles.",
            "plan": ["Use your emotional stability as a foundation for taking on challenging projects and responsibilities.|Consider high-pressure careers like Emergency Medicine, Air Traffic Control, Investment Banking, or Military Services where your calm nature is invaluable.|Continue maintaining your mental health through regular exercise, sleep, and healthy coping mechanisms.|Help peers who struggle with stress by sharing your coping strategies and providing emotional support."]
        },
        "Moderate": {
            "analysis": "Your moderate emotional stability score indicates that you generally manage your emotions well but may sometimes be affected by stress, anxiety, or emotional fluctuations during particularly challenging periods. Building stronger stress management techniques will help you maintain your equilibrium across all situations.",
            "plan": ["Practice stress management techniques like deep breathing, meditation, or mindfulness regularly.|Identify your personal stress triggers and develop specific coping strategies for each.|Maintain regular physical exercise, sleep schedules, and social connections as foundations of emotional well-being.|Consider journaling or talking to a trusted person when you feel emotionally overwhelmed to process your feelings constructively."]
        },
        "Low": {
            "analysis": "Your score suggests that emotional regulation can be challenging for you. You may experience significant stress, anxiety, or emotional fluctuations that can impact your performance and well-being. This is an important area for development, as emotional stability significantly influences academic performance, relationships, and career success.",
            "plan": ["Start a daily mindfulness or meditation practice — even 5 minutes can significantly improve emotional regulation over time.|Seek support from a school counselor, therapist, or trusted adult who can teach you coping strategies.|Develop a personal 'calm-down toolkit' with techniques like deep breathing, progressive muscle relaxation, or physical activity.|Identify activities that help you feel grounded and make them a regular part of your routine (sports, music, nature walks, art)."]
        }
    },
    "risk_appetite": {
        "label": "Risk Appetite",
        "meaning": "Risk appetite measures your willingness to take calculated risks, step outside your comfort zone, and embrace uncertainty. It reflects your tolerance for ambiguity and your comfort with situations where outcomes are unpredictable.",
        "High": {
            "analysis": "Your high risk appetite score indicates a bold, adventurous nature. You are comfortable with uncertainty and willing to take calculated risks for potential rewards. You likely prefer dynamic, fast-paced environments over predictable routines. This trait is valuable for entrepreneurship, innovation, and leadership roles that require bold decision-making.",
            "plan": ["Channel your risk-taking nature into constructive ventures like entrepreneurship competitions or startup projects.|Learn risk assessment frameworks to make your bold moves more calculated and strategic.|Consider careers that reward calculated risk-taking: Entrepreneurship, Venture Capital, Trading, Journalism, or Emergency Services.|Balance your risk appetite with thorough preparation — even bold moves benefit from research and planning."]
        },
        "Moderate": {
            "analysis": "Your moderate risk appetite indicates a balanced approach to risk. You can take calculated risks when the situation warrants it but prefer to have some certainty and planning before making bold moves. This balanced approach protects you from reckless decisions while still allowing for growth and new opportunities.",
            "plan": ["Practice taking small, calculated risks in safe environments (trying new activities, speaking up in class) to gradually expand your comfort zone.|Learn to distinguish between reckless risks and calculated opportunities by assessing potential outcomes.|Explore careers that offer stability with opportunities for innovation, such as Corporate Strategy, Product Management, or Healthcare.|Develop your ability to assess risk-reward ratios to make increasingly confident decisions."]
        },
        "Low": {
            "analysis": "Your score suggests a preference for safety, stability, and predictability. You tend to avoid unnecessary risks and prefer well-defined paths with clear outcomes. While this caution protects you from impulsive decisions, developing some comfort with calculated risk-taking will expand your opportunities for growth and success.",
            "plan": ["Start with very small risks — try a new food, speak up in class, or join a new activity to gradually build comfort with uncertainty.|Practice the 'what's the worst that can happen?' exercise to put risks in perspective.|Explore careers that offer stability and clear progression: Government Services, Banking, Teaching, Accounting, or Quality Assurance.|Remember that avoiding all risk is itself risky — sometimes not trying is the biggest risk of all."]
        }
    },
    "self_discipline": {
        "label": "Self Discipline",
        "meaning": "Self discipline measures your ability to control impulses, maintain focus on long-term goals, and consistently follow through on commitments. It reflects your capacity for self-regulation, time management, and sustained effort without external pressure.",
        "High": {
            "analysis": "Your high self-discipline score indicates excellent self-regulation abilities. You are likely organized, punctual, and consistent in your work habits. You can resist short-term temptations in favor of long-term goals and maintain focus even on tedious tasks. This trait is a powerful predictor of academic and career success across all fields.",
            "plan": ["Use your self-discipline to build mastery in your chosen field through consistent daily practice and study.|Help peers develop their own discipline by sharing your strategies and routines.|Consider demanding fields like Medicine, Law, Civil Services, or Research that require sustained disciplined effort over many years.|Ensure you build in relaxation and fun alongside your disciplined routine to prevent burnout."]
        },
        "Moderate": {
            "analysis": "Your moderate self-discipline score indicates that you generally manage your time and commitments well but may sometimes struggle with procrastination or maintaining focus on less interesting tasks. Strengthening your self-discipline habits will significantly enhance your academic performance and career readiness.",
            "plan": ["Create a structured daily routine with specific study times, breaks, and deadlines to build consistency.|Use the 'two-minute rule' — if a task takes less than two minutes, do it immediately to prevent procrastination.|Try habit-stacking: attach new disciplined habits to existing ones (e.g., study for 30 minutes right after dinner).|Remove distractions during focused work time — put your phone in another room and use website blockers if needed."]
        },
        "Low": {
            "analysis": "Your score suggests that maintaining consistent discipline and self-regulation can be challenging. You may experience frequent procrastination, difficulty staying focused, or trouble following through on commitments. Developing self-discipline is one of the most impactful changes you can make for your academic and career success.",
            "plan": ["Start with one small daily habit (like making your bed or reading for 10 minutes) and build consistency before adding more.|Use external accountability — study with a partner, set public commitments, or use apps that track your habits.|Break overwhelming tasks into tiny steps and focus on completing just the first step to overcome procrastination.|Seek support from a mentor, counselor, or parent who can help you develop structured routines and stay accountable."]
        }
    },
    # --- APTITUDE ---
    "verbal_reasoning": {
        "label": "Verbal Reasoning",
        "meaning": "Verbal reasoning measures your ability to understand, analyze, and draw conclusions from written text and spoken language. It reflects your capacity for comprehension, vocabulary usage, critical reading, and logical deduction from verbal information.",
        "High": {"analysis": "Your strong verbal reasoning indicates excellent language comprehension and analytical reading skills. You can quickly extract meaning from complex texts, understand nuanced arguments, and communicate your ideas clearly. This ability is invaluable in careers that require effective communication, persuasion, and written expression.", "plan": ["Expand your reading to include diverse genres — fiction, non-fiction, editorials, and academic papers.|Practice debate and public speaking to leverage your verbal strengths in real-time communication.|Consider careers in Law, Journalism, Writing, Teaching, Translation, or Public Relations that heavily utilize verbal skills.|Develop writing skills through regular journaling, blogging, or creative writing to complement your reading abilities."]},
        "Moderate": {"analysis": "Your moderate verbal reasoning indicates competent language skills with room for growth. You can handle standard texts effectively but may find complex or technical writing more challenging. Consistent reading and vocabulary building will strengthen this foundational ability.", "plan": ["Read widely and regularly — aim for at least 30 minutes of focused reading daily.|Practice summarizing what you read to improve comprehension and analytical skills.|Learn new words daily through vocabulary apps or word-of-the-day services.|Practice writing essays or summaries to strengthen your ability to express ideas clearly."]},
        "Low": {"analysis": "Your score suggests that verbal reasoning is not your strongest area. You may find complex reading or verbal analysis challenging compared to visual, numerical, or hands-on tasks. While this is an area for development, remember that many successful careers emphasize other cognitive abilities.", "plan": ["Start with reading materials you enjoy (comics, sports magazines, short stories) and gradually increase complexity.|Use audiobooks and podcasts as alternative ways to strengthen verbal processing.|Practice reading comprehension exercises regularly to build this skill systematically.|Focus on your stronger aptitude areas while gradually building verbal skills as a supporting competency."]},
    },
    "numerical_ability": {
        "label": "Numerical Ability",
        "meaning": "Numerical ability measures your comfort and skill with numbers, mathematical operations, data interpretation, and quantitative reasoning. It reflects your capacity to work with numerical data, perform calculations, and draw conclusions from quantitative information.",
        "High": {"analysis": "Your strong numerical ability indicates excellent quantitative reasoning skills. You are comfortable working with numbers, data, and mathematical concepts. You likely find calculations intuitive and can quickly interpret numerical information. This aptitude opens doors to many high-demand careers in finance, engineering, and data sciences.", "plan": ["Deepen your mathematical skills through advanced courses, olympiad preparation, or competitive math.|Learn data analysis tools like Excel, Python, or R to apply your numerical abilities practically.|Consider careers in Finance, Engineering, Data Science, Actuarial Science, Accounting, or Economics.|Practice mental math and estimation skills to make your numerical ability faster and more intuitive."]},
        "Moderate": {"analysis": "Your moderate numerical ability indicates competent quantitative skills with potential for growth. You can handle standard mathematical tasks but may find complex calculations or data analysis more challenging. Building stronger numerical foundations will expand your career options significantly.", "plan": ["Practice regular math exercises focusing on areas where you feel less confident.|Use real-world applications (budgeting, measuring, cooking) to make numerical practice more engaging.|Consider careers that use moderate math alongside other skills, such as Marketing, Healthcare, or Architecture.|Use online tools and apps designed to make math practice more engaging and gradually build your confidence."]},
        "Low": {"analysis": "Your score suggests that working with numbers is not your strongest area. You may find mathematical tasks tedious or challenging compared to verbal or creative work. While many careers don't require advanced math, basic numerical literacy is important for personal and professional life.", "plan": ["Focus on practical math skills (budgeting, percentages, basic data interpretation) that are useful in everyday life.|Use visual and hands-on approaches to math that may be more engaging than abstract calculations.|Explore careers that emphasize your stronger aptitudes while requiring minimal advanced mathematics.|Consider using calculators and spreadsheets as tools — competence with numerical tools is just as valuable as mental math."]},
    },
    "logical_reasoning": {
        "label": "Logical Reasoning",
        "meaning": "Logical reasoning measures your ability to identify patterns, draw valid conclusions, and solve problems through systematic thinking. It reflects your capacity for deductive and inductive reasoning, pattern recognition, and structured problem-solving.",
        "High": {"analysis": "Your strong logical reasoning indicates excellent pattern recognition and systematic problem-solving abilities. You can identify relationships between concepts, draw valid conclusions from premises, and approach problems methodically. This is a core cognitive ability valued across virtually all professional fields.", "plan": ["Challenge yourself with logic puzzles, coding problems, and strategic games to keep your reasoning skills sharp.|Learn programming (Python, Java) as it directly exercises and rewards logical thinking.|Consider careers in Software Engineering, Law, Strategy Consulting, Research, or Detective Work that heavily rely on logical reasoning.|Practice explaining your reasoning process to others — teaching logic helps you master it."]},
        "Moderate": {"analysis": "Your moderate logical reasoning indicates competent problem-solving abilities with room for enhancement. You can work through logical problems but may sometimes find complex multi-step reasoning challenging. Regular practice will strengthen this important cognitive skill.", "plan": ["Practice logic puzzles (Sudoku, crosswords, brain teasers) regularly to build your reasoning abilities.|Learn to break complex problems into smaller logical steps to make them more manageable.|Take courses in critical thinking or formal logic to develop structured reasoning skills.|Practice identifying logical fallacies in everyday arguments to sharpen your analytical thinking."]},
        "Low": {"analysis": "Your score suggests that structured logical reasoning is not your primary cognitive strength. You may prefer intuitive, creative, or practical approaches to problem-solving over systematic logical analysis. While logical skills can be developed, focusing on your natural strengths while building basic logical competency is a wise approach.", "plan": ["Practice simple logic exercises daily to gradually build your reasoning capacity.|Use visual aids like flowcharts and diagrams to support your logical thinking process.|Learn basic if-then reasoning and practice applying it to everyday decisions.|Explore careers that value your stronger aptitudes while requiring less intense logical analysis."]},
    },
    "abstract_thinking": {
        "label": "Abstract Thinking",
        "meaning": "Abstract thinking measures your ability to understand and work with concepts, ideas, and theories that are not directly tied to concrete physical experiences. It reflects your capacity for theoretical reasoning, conceptual understanding, and imaginative problem-solving.",
        "High": {"analysis": "Your strong abstract thinking indicates an excellent ability to work with theoretical concepts and ideas. You can understand complex theories, think hypothetically, and grasp concepts that don't have immediate physical representations. This cognitive ability is essential for advanced academic work and careers that involve complex conceptual frameworks.", "plan": ["Explore philosophical texts, theoretical physics, or advanced mathematics to exercise your abstract thinking.|Consider careers in Research, Philosophy, Theoretical Sciences, Strategy, or Architecture that require strong conceptual thinking.|Practice translating abstract ideas into practical applications to make your thinking more actionable.|Engage in creative activities like writing or art that allow abstract expression."]},
        "Moderate": {"analysis": "Your moderate abstract thinking indicates a balanced ability to work with both concrete and conceptual ideas. You can grasp theoretical concepts but may prefer practical applications over pure abstraction. This balance is valuable in careers that require both theoretical understanding and practical implementation.", "plan": ["Practice connecting abstract concepts to real-world examples to strengthen your theoretical understanding.|Explore subjects that blend theory with practice, such as applied sciences, design, or business strategy.|Use visual tools like mind maps and diagrams to make abstract concepts more tangible.|Read widely across different subjects to expose yourself to diverse conceptual frameworks."]},
        "Low": {"analysis": "Your score suggests a preference for concrete, practical thinking over abstract conceptualization. You likely learn best through hands-on experience and real-world examples rather than theoretical lectures. While this practical orientation is valuable in many careers, developing some comfort with abstract thinking will broaden your capabilities.", "plan": ["Use analogies and real-world examples to understand abstract concepts in your studies.|Focus on practical, hands-on learning approaches that align with your concrete thinking style.|Explore careers that value practical skills: trades, technician roles, agriculture, culinary arts, or applied technology.|Practice 'what if' thinking exercises to gradually develop comfort with hypothetical scenarios."]},
    },
    "spatial_visualization": {
        "label": "Spatial Visualization",
        "meaning": "Spatial visualization measures your ability to mentally manipulate two- and three-dimensional objects, understand spatial relationships, and visualize how things fit together. It reflects your capacity for visual thinking, design sense, and geometric reasoning.",
        "High": {"analysis": "Your strong spatial visualization indicates excellent visual-spatial intelligence. You can mentally rotate objects, understand spatial relationships, and visualize complex structures. This ability is essential for careers in design, engineering, architecture, and many creative fields. You likely find maps, diagrams, and 3D models intuitive to understand.", "plan": ["Practice 3D modeling with tools like SketchUp, Blender, or AutoCAD to develop practical spatial skills.|Explore careers in Architecture, Interior Design, Civil Engineering, Mechanical Engineering, Animation, or Graphic Design.|Engage in activities like building models, solving puzzles, or playing strategic games that exercise spatial thinking.|Study technical drawing and visualization techniques to formalize your natural spatial abilities."]},
        "Moderate": {"analysis": "Your moderate spatial visualization indicates competent visual-spatial skills with room for growth. You can understand basic spatial relationships and diagrams but may find complex 3D visualization more challenging. Regular practice with visual-spatial tasks will strengthen this ability.", "plan": ["Practice reading and creating diagrams, maps, and technical drawings regularly.|Try 3D puzzle games or model building to develop hands-on spatial skills.|Use visualization exercises — practice mentally rotating objects or imagining room layouts.|Explore how spatial skills complement your other aptitudes for unique career combinations."]},
        "Low": {"analysis": "Your score suggests that spatial visualization is not your primary cognitive strength. You may find it challenging to mentally rotate objects or understand complex diagrams. While this is an area for development, many successful careers emphasize verbal, numerical, or interpersonal skills over spatial abilities.", "plan": ["Use physical models and 3D objects to supplement what you find difficult to visualize mentally.|Focus on careers that emphasize your stronger aptitudes rather than spatial skills.|Practice simple spatial exercises (jigsaw puzzles, Tetris) to gradually build your spatial awareness.|Use technology and tools to assist with spatial tasks when needed in your studies or work."]},
    },
    "technological_understanding": {
        "label": "Technological Understanding",
        "meaning": "Technological understanding measures your comfort with and comprehension of technology, digital tools, and technical systems. It reflects your ability to understand how technology works, learn new tools quickly, and apply technology to solve problems.",
        "High": {"analysis": "Your strong technological understanding indicates a natural comfort with technology and digital systems. You likely learn new tools quickly, understand how technical systems work, and enjoy exploring new technologies. In today's digital world, this aptitude is increasingly valuable across virtually all career fields.", "plan": ["Learn programming, web development, or app development to transform your tech understanding into practical skills.|Stay updated with emerging technologies like AI, blockchain, cloud computing, and IoT.|Consider careers in Software Development, IT Management, Data Analytics, Cybersecurity, or Tech Entrepreneurship.|Help others in your community understand and use technology — teaching reinforces your own understanding."]},
        "Moderate": {"analysis": "Your moderate technological understanding indicates competent digital skills with potential for growth. You can use standard technology tools effectively but may not deeply understand how they work under the hood. Building stronger technical skills will significantly enhance your career readiness in an increasingly digital world.", "plan": ["Take online courses in basic programming, data analysis, or digital marketing to strengthen your tech skills.|Practice using new apps and tools regularly to expand your technology comfort zone.|Explore how technology is transforming your areas of interest — every field is being digitized.|Develop competency with productivity tools (spreadsheets, presentation software, project management tools) as baseline skills."]},
        "Low": {"analysis": "Your score suggests that technology is not your strongest area. You may find learning new software challenging or prefer traditional methods over digital tools. While deep technical expertise isn't needed in every career, basic digital literacy is essential in today's workplace.", "plan": ["Start with the basics — become proficient with email, word processing, spreadsheets, and internet research.|Ask tech-savvy friends or family to teach you useful digital skills in a supportive environment.|Take beginner-friendly online courses that introduce technology concepts at a comfortable pace.|Focus on learning the specific tech tools relevant to your chosen career path rather than trying to learn everything."]},
    },
    "perceptual_speed": {
        "label": "Perceptual Speed & Accuracy",
        "meaning": "Perceptual speed measures your ability to quickly and accurately compare information, identify differences, and process visual data. It reflects your capacity for detail-oriented work, rapid information processing, and attention to accuracy.",
        "High": {"analysis": "Your strong perceptual speed indicates excellent ability to process information quickly and accurately. You can spot differences, identify patterns, and process detailed data rapidly. This aptitude is valuable in careers that require precision, attention to detail, and quick information processing.", "plan": ["Practice speed-accuracy tasks like proofreading, data verification, and spot-the-difference exercises to maintain your edge.|Consider careers in Quality Assurance, Auditing, Medical Diagnosis, Air Traffic Control, or Financial Analysis where speed and accuracy are critical.|Develop complementary skills like data analysis or visual design that leverage your perceptual strengths.|Use your quick processing ability to take on tasks that others find tedious but are essential for success."]},
        "Moderate": {"analysis": "Your moderate perceptual speed indicates competent information processing abilities. You can handle standard detail-oriented tasks but may slow down with very complex or high-volume data processing. Regular practice will help improve your speed and accuracy.", "plan": ["Practice detail-oriented exercises like proofreading, sudoku, or spot-the-difference puzzles regularly.|Develop systematic checking habits — create checklists and review procedures for important work.|Focus on accuracy first, then gradually increase your processing speed.|Use tools and technology to support your information processing when handling large amounts of data."]},
        "Low": {"analysis": "Your score suggests that rapid, detail-oriented information processing is not your primary strength. You may work more slowly through detailed tasks or occasionally miss small details. While this is an area for development, many successful careers emphasize big-picture thinking over rapid detail processing.", "plan": ["Practice mindfulness exercises to improve your attention to detail and focus.|Develop checking systems and review procedures to catch errors before they become problems.|Use technology tools that help identify errors (spell-check, formula auditing, etc.) to supplement your natural abilities.|Focus on careers that value strategic thinking, creativity, or interpersonal skills over rapid detail processing."]},
    },
    # --- EMOTIONAL QUOTIENT ---
    "emotional_awareness": {
        "label": "Emotional Self-Awareness",
        "meaning": "Emotional self-awareness measures your ability to recognize, understand, and label your own emotions as they occur. It reflects your capacity for introspection, understanding your emotional triggers, and recognizing how your feelings influence your thoughts and behavior.",
        "High": {"analysis": "Your high emotional self-awareness indicates a strong ability to recognize and understand your own emotions. You can identify what you are feeling and why, which is the foundation of all emotional intelligence. This self-knowledge helps you make better decisions, communicate more authentically, and manage your emotional responses effectively.", "plan": ["Continue developing your emotional vocabulary to describe increasingly nuanced emotional states.|Practice mindfulness meditation to deepen your emotional self-awareness even further.|Use journaling to track emotional patterns and understand your triggers and responses.|Consider careers in Counseling, Psychology, Human Resources, or Leadership where emotional awareness is a key asset."]},
        "Moderate": {"analysis": "Your moderate emotional self-awareness indicates that you generally understand your emotions but may sometimes be caught off-guard by unexpected feelings or struggle to identify complex emotional states. Building stronger emotional awareness will enhance your overall emotional intelligence and interpersonal effectiveness.", "plan": ["Start a feelings journal — write about your emotions daily to build awareness of your emotional patterns.|Practice pausing before reacting to strong emotions to create space for self-awareness.|Learn to name your emotions specifically (frustrated vs. angry, anxious vs. nervous) to build emotional vocabulary.|Discuss your feelings with trusted friends or family members to gain external perspectives on your emotional patterns."]},
        "Low": {"analysis": "Your score suggests that recognizing and understanding your own emotions can be challenging. You may sometimes feel confused about your emotional state or be caught off-guard by strong feelings. Developing emotional self-awareness is the first and most important step in building overall emotional intelligence.", "plan": ["Begin a daily emotional check-in — take 2 minutes each day to ask yourself 'How am I feeling right now?' and write it down.|Learn basic emotion categories (happy, sad, angry, afraid, surprised, disgusted) as a starting framework.|Pay attention to physical sensations associated with emotions (tight chest = anxiety, warm face = embarrassment) as physical cues.|Consider talking to a school counselor or therapist who can help you develop emotional awareness in a safe, supportive environment."]},
    },
    "emotional_regulation": {
        "label": "Emotional Regulation",
        "meaning": "Emotional regulation measures your ability to manage, control, and appropriately express your emotions. It reflects your capacity to calm yourself when upset, maintain composure under pressure, and choose your emotional responses rather than being controlled by them.",
        "High": {"analysis": "Your high emotional regulation score indicates excellent ability to manage your emotional responses. You can stay calm under pressure, recover from setbacks, and maintain appropriate emotional expression. This maturity in emotional management is a significant asset in professional and personal settings, making you reliable and resilient.", "plan": ["Continue practicing stress management techniques to maintain your emotional regulation skills.|Share your emotional regulation strategies with peers who may struggle in this area.|Consider high-pressure careers where emotional regulation is essential: Medicine, Emergency Services, Negotiation, or Leadership.|Be mindful that over-regulation (suppressing emotions) is different from healthy regulation — ensure you still express your feelings authentically."]},
        "Moderate": {"analysis": "Your moderate emotional regulation indicates that you generally manage your emotions well but may sometimes struggle during intense or prolonged stress. Building stronger regulation techniques will help you maintain composure even in the most challenging situations.", "plan": ["Learn and practice specific regulation techniques: deep breathing, counting to ten, progressive muscle relaxation.|Identify your emotional triggers and develop pre-planned responses for when they occur.|Build a 'calm-down kit' of activities that help you regulate (music, walking, deep breathing, talking to someone).|Practice the pause — when you feel a strong emotion, take 3 deep breaths before responding to any situation."]},
        "Low": {"analysis": "Your score suggests that managing emotional responses can be challenging for you. You may experience emotional outbursts, difficulty calming down when upset, or prolonged negative emotional states. Developing emotional regulation skills is crucial for academic success, healthy relationships, and career readiness.", "plan": ["Start with physical regulation: exercise, deep breathing, or splashing cold water on your face can quickly reduce emotional intensity.|Develop an emotional first-aid plan — identify 3 things you can do when you feel overwhelmed (call someone, take a walk, listen to music).|Consider working with a counselor or therapist who specializes in teaching emotional regulation strategies.|Practice the STOP technique: Stop what you're doing, Take a breath, Observe your emotions, Proceed thoughtfully."]},
    },
    "empathy": {
        "label": "Empathy",
        "meaning": "Empathy measures your ability to understand, share, and respond to the feelings and perspectives of others. It reflects your capacity to put yourself in someone else's shoes, sense their emotional state, and respond with appropriate care and understanding.",
        "High": {"analysis": "Your high empathy score indicates a remarkable ability to understand and share the feelings of others. You naturally tune into people's emotional states, understand their perspectives, and respond with genuine care. This emotional sensitivity makes you an excellent friend, teammate, and potential leader. Empathy is increasingly recognized as a critical skill in the modern workplace.", "plan": ["Channel your empathy into meaningful roles: volunteering, peer mentoring, or community service.|Develop healthy boundaries to prevent empathy fatigue — caring for others is important, but so is protecting your own emotional well-being.|Consider careers where empathy is essential: Counseling, Medicine, Teaching, Social Work, Human Resources, or Customer Success.|Learn to balance empathy with objectivity — sometimes the most helpful response requires tough love rather than pure emotional support."]},
        "Moderate": {"analysis": "Your moderate empathy score indicates a balanced ability to understand others' feelings. You can empathize when needed but may not always naturally tune into subtle emotional cues. This balance allows you to be compassionate without being overwhelmed by others' emotions.", "plan": ["Practice active listening — focus entirely on the speaker without planning your response while they talk.|Read fiction — studies show that reading stories increases empathy by helping you experience diverse perspectives.|Practice asking 'How does this person feel?' in different social situations to build your empathetic awareness.|Volunteer for community service to expose yourself to diverse life experiences that naturally build empathy."]},
        "Low": {"analysis": "Your score suggests that understanding others' emotions and perspectives does not come as naturally to you. You may sometimes miss emotional cues or find it challenging to see situations from another person's point of view. While empathy can be developed, it requires conscious effort and practice.", "plan": ["Practice perspective-taking — when you disagree with someone, try to genuinely understand their position before responding.|Watch emotional films or read personal stories to exercise your empathetic abilities in low-pressure situations.|Ask people directly how they feel rather than trying to guess — this honest approach builds connection even when natural empathy is lower.|Practice the phrase 'That must be really difficult' when someone shares a problem — acknowledging emotions even when you don't fully feel them builds trust."]},
    },
    "social_skills": {
        "label": "Social Skills",
        "meaning": "Social skills measures your ability to build and maintain relationships, communicate effectively in social settings, and navigate interpersonal dynamics. It reflects your capacity for networking, collaboration, conflict resolution, and social influence.",
        "High": {"analysis": "Your high social skills score indicates excellent interpersonal abilities. You can build relationships quickly, communicate effectively across different social contexts, and navigate group dynamics smoothly. You are likely popular among peers and comfortable in diverse social settings. These skills are invaluable in virtually every career path.", "plan": ["Continue developing your network by meeting people from diverse backgrounds and fields.|Learn advanced social skills like negotiation, persuasion, and public speaking to elevate your interpersonal effectiveness.|Consider careers where social skills are paramount: Sales, HR, Public Relations, Teaching, Consulting, or Politics.|Help others who are less socially confident — mentoring builds your skills while helping your community."]},
        "Moderate": {"analysis": "Your moderate social skills indicate competent interpersonal abilities with room for growth. You can interact effectively in familiar social settings but may feel less comfortable in new or challenging social situations. Building confidence in diverse social contexts will significantly enhance your career prospects.", "plan": ["Practice social interactions in low-pressure settings to build your confidence gradually.|Learn and practice conversation starters, active listening, and body language reading.|Join clubs, activities, or groups where you can develop social skills with shared-interest peers.|Practice introducing yourself to new people at least once a week to expand your comfort zone."]},
        "Low": {"analysis": "Your score suggests that social interactions can be challenging or uncomfortable for you. You may find it difficult to initiate conversations, build new relationships, or navigate complex social dynamics. While this is an area for development, remember that social skills can be learned and improved with practice, just like any other skill.", "plan": ["Start with one-on-one interactions rather than group settings, which can be less overwhelming.|Practice scripted social interactions (ordering food, asking for directions) to build confidence.|Join interest-based groups where social interaction happens naturally around a shared activity.|Consider working with a counselor or coach who can help you develop specific social strategies in a supportive environment."]},
    },
    "motivation": {
        "label": "Motivation",
        "meaning": "Motivation measures your internal drive to achieve goals, pursue excellence, and maintain effort over time. It reflects your capacity for self-motivation, goal orientation, optimism, and the ability to find purpose and meaning in your work.",
        "High": {"analysis": "Your high motivation score indicates a strong internal drive to achieve and excel. You set goals, pursue them with energy, and maintain enthusiasm even during challenging periods. This self-motivation is one of the most powerful predictors of success, as it sustains effort long after initial excitement fades. You likely set high standards for yourself and are driven by a desire to improve continuously.", "plan": ["Set challenging but achievable long-term goals that align with your values and interests to maintain your motivation.|Learn to motivate others — your energy and drive can inspire teams and communities.|Consider demanding careers that reward sustained motivation: Medicine, Research, Entrepreneurship, Competitive Sports, or Civil Services.|Practice self-compassion alongside your drive — high motivation should be balanced with kindness to yourself during setbacks."]},
        "Moderate": {"analysis": "Your moderate motivation score indicates that you can be driven and focused when interested in a task but may struggle with motivation for activities that don't align with your interests. Finding your personal 'why' — the deeper purpose behind your goals — will help sustain motivation even through less exciting phases.", "plan": ["Identify your core values and connect your goals to those values for more sustainable motivation.|Create a vision board or goal tracker that keeps your long-term aspirations visible and top of mind.|Find an accountability partner who can help you stay motivated during low-energy periods.|Experiment with different reward systems to find what motivates you best (social recognition, personal achievements, tangible rewards)."]},
        "Low": {"analysis": "Your score suggests that sustaining motivation can be challenging for you. You may start projects with enthusiasm but find it hard to maintain effort over time, especially when tasks become routine or challenging. Developing motivation strategies is crucial for academic success and career growth.", "plan": ["Start by finding activities that naturally excite you — motivation is easiest when you genuinely care about what you're doing.|Use the 'just start' technique — commit to working on a task for just 5 minutes, and momentum often follows.|Create external motivation structures: study groups, deadlines, rewards, and public commitments.|Break your goals into the smallest possible steps — each completed micro-step builds momentum and confidence."]},
    },
    "conflict_management": {
        "label": "Conflict Management",
        "meaning": "Conflict management measures your ability to handle disagreements, resolve disputes, and navigate interpersonal tensions constructively. It reflects your capacity for negotiation, mediation, assertiveness without aggression, and finding win-win solutions.",
        "High": {"analysis": "Your high conflict management score indicates excellent ability to handle disagreements constructively. You can navigate tensions without escalation, find common ground, and help resolve disputes effectively. This is a mature and valuable skill that is essential for leadership, teamwork, and professional success.", "plan": ["Develop formal negotiation and mediation skills through courses or training programs.|Practice helping peers resolve their conflicts as an informal mediator to build experience.|Consider careers where conflict resolution is key: Law, HR, Diplomacy, Mediation, Counseling, or Management.|Continue developing your assertiveness to ensure you address conflicts proactively rather than avoiding them."]},
        "Moderate": {"analysis": "Your moderate conflict management score indicates that you can handle some disagreements effectively but may struggle with intense or complex conflicts. You might sometimes avoid confrontation or become frustrated during prolonged disputes. Building stronger conflict resolution techniques will enhance your interpersonal effectiveness.", "plan": ["Learn specific conflict resolution techniques like the 'I-statement' method (I feel... when you... because...).|Practice addressing small disagreements directly rather than letting them build up into larger conflicts.|Study negotiation basics — understanding how to find win-win solutions transforms how you approach disagreements.|Role-play difficult conversations with a trusted friend or mentor to build confidence in handling real conflicts."]},
        "Low": {"analysis": "Your score suggests that handling conflicts is challenging for you. You may either avoid confrontation entirely or react emotionally during disagreements, both of which can strain relationships and hinder professional growth. Developing conflict management skills is essential for building healthy personal and professional relationships.", "plan": ["Start by practicing disagreeing respectfully in low-stakes situations to build your confidence with conflict.|Learn the difference between assertive (healthy) and aggressive (harmful) communication styles.|Develop a personal conflict response plan: what will you do when you feel conflict arising? (Take a breath, use I-statements, listen first).|Seek guidance from a counselor or mentor who can help you develop specific strategies for handling disagreements constructively."]},
    },
}

# Career recommendation mapping based on score patterns
CAREER_MATCHES = {
    "high_creative_high_arts": ["Graphic Designer", "UX/UI Designer", "Film Director", "Architect", "Fashion Designer"],
    "high_analytical_high_stem": ["Software Engineer", "Data Scientist", "Research Scientist", "Mechanical Engineer", "Actuary"],
    "high_people_high_healthcare": ["Doctor (MBBS)", "Clinical Psychologist", "Physiotherapist", "Public Health Specialist", "Nurse"],
    "high_people_high_social": ["Social Worker", "School Teacher", "HR Manager", "Counselor", "NGO Manager"],
    "high_admin_high_business": ["Chartered Accountant", "Banking Officer", "Operations Manager", "Company Secretary", "Compliance Officer"],
    "high_creative_high_stem": ["AI/ML Engineer", "Game Developer", "Product Designer", "Biomedical Engineer", "Robotics Engineer"],
    "high_analytical_high_business": ["Financial Analyst", "Management Consultant", "Investment Banker", "Business Analyst", "Actuary"],
    "high_people_high_business": ["Marketing Manager", "Sales Manager", "Event Manager", "HR Manager", "Public Relations Officer"],
    "moderate_all": ["Product Manager", "Project Manager", "Business Analyst", "Education Counselor", "Healthcare Administrator"],
}


class ComprehensiveReportGenerator:
    """Generate detailed 18-20 page psychometric assessment reports"""

    def __init__(self):
        self.page_width, self.page_height = A4
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
        # Color palette
        self.PRIMARY = '#1A2B4B'
        self.SECONDARY = '#5D7A68'
        self.ACCENT = '#C87961'
        self.LIGHT_BG = '#F9F8F6'
        self.LIGHT_GREEN = '#E8F5E9'
        self.LIGHT_BLUE = '#E3F2FD'
        self.LIGHT_AMBER = '#FFF8E1'

    def _create_custom_styles(self):
        self.styles.add(ParagraphStyle(name='ReportTitle', parent=self.styles['Heading1'], fontSize=28, textColor=colors.HexColor('#1A2B4B'), spaceAfter=20, alignment=TA_CENTER, fontName='Helvetica-Bold'))
        self.styles.add(ParagraphStyle(name='SectionHeading', parent=self.styles['Heading2'], fontSize=18, textColor=colors.HexColor('#1A2B4B'), spaceAfter=12, spaceBefore=16, fontName='Helvetica-Bold'))
        self.styles.add(ParagraphStyle(name='SubsectionHeading', parent=self.styles['Heading3'], fontSize=14, textColor=colors.HexColor('#1A2B4B'), spaceAfter=8, spaceBefore=10, fontName='Helvetica-Bold'))
        self.styles.add(ParagraphStyle(name='TraitHeading', parent=self.styles['Heading3'], fontSize=13, textColor=colors.HexColor('#5D7A68'), spaceAfter=6, spaceBefore=10, fontName='Helvetica-Bold'))
        self.styles.add(ParagraphStyle(name='ReportBody', parent=self.styles['Normal'], fontSize=10, textColor=colors.HexColor('#1A1A1A'), alignment=TA_JUSTIFY, spaceAfter=8, leading=14))
        self.styles.add(ParagraphStyle(name='SmallLabel', parent=self.styles['Normal'], fontSize=9, textColor=colors.HexColor('#666666'), spaceAfter=4, leading=12))
        self.styles.add(ParagraphStyle(name='BulletItem', parent=self.styles['Normal'], fontSize=10, textColor=colors.HexColor('#2A2A2A'), alignment=TA_LEFT, spaceAfter=4, leading=13, leftIndent=20, bulletIndent=10))

    def _get_band(self, score):
        if score < 40: return "Low"
        elif score < 70: return "Moderate"
        return "High"

    def _add_header_footer(self, canvas_obj, doc):
        canvas_obj.saveState()
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(colors.HexColor('#888888'))
        canvas_obj.drawString(50, A4[1] - 28, "BoatMyCareer.com | Career Discovery Report")
        canvas_obj.drawRightString(A4[0] - 50, 28, f"Page {doc.page}")
        canvas_obj.setStrokeColor(colors.HexColor('#DDDDDD'))
        canvas_obj.line(50, A4[1] - 32, A4[0] - 50, A4[1] - 32)
        canvas_obj.line(50, 36, A4[0] - 50, 36)
        canvas_obj.restoreState()

    def _create_bar_chart(self, scores, title, figsize=(6, 3)):
        try:
            labels = [TRAIT_DATA.get(k, {}).get('label', k.replace('_', ' ').title()) for k in scores.keys()]
            values = list(scores.values())
            fig, ax = plt.subplots(figsize=figsize)
            bar_colors = ['#5D7A68' if v >= 70 else '#C87961' if v >= 40 else '#94A3B8' for v in values]
            bars = ax.barh(labels, values, color=bar_colors, height=0.6, edgecolor='white', linewidth=0.5)
            for i, v in enumerate(values):
                ax.text(v + 1.5, i, f'{v:.0f}%', va='center', fontsize=8, fontweight='bold')
            ax.set_xlim(0, 110)
            ax.set_title(title, fontsize=11, fontweight='bold', color='#1A2B4B', pad=10)
            ax.set_xlabel('Score (%)', fontsize=9)
            ax.grid(axis='x', alpha=0.2)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.tight_layout()
            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            buf.seek(0)
            plt.close()
            h = max(2.2, 0.4 * len(labels) + 1.0)
            return RLImage(buf, width=5.2*inch, height=h*inch)
        except Exception as e:
            print(f"Error creating bar chart: {e}")
            return None

    def _create_radar_chart(self, all_scores):
        try:
            dims = ['Orientation', 'Interest', 'Personality', 'Aptitude', 'EQ']
            vals = []
            for t in ['orientation', 'interest', 'personality', 'aptitude', 'eq']:
                s = all_scores.get(t, {}).get('scores', {})
                vals.append(sum(s.values()) / len(s) if s else 50)
            angles = np.linspace(0, 2 * np.pi, len(dims), endpoint=False).tolist()
            vals += vals[:1]
            angles += angles[:1]
            fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(projection='polar'))
            ax.plot(angles, vals, 'o-', linewidth=2.5, color='#1A2B4B', markersize=6)
            ax.fill(angles, vals, alpha=0.2, color='#5D7A68')
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(dims, size=10, fontweight='bold')
            ax.set_ylim(0, 100)
            ax.set_yticks([20, 40, 60, 80, 100])
            ax.set_yticklabels(['20', '40', '60', '80', '100'], size=7, color='#888')
            ax.grid(True, alpha=0.3)
            ax.set_title('Your 5-Dimensional Profile', size=13, fontweight='bold', color='#1A2B4B', pad=20)
            for i, (angle, val) in enumerate(zip(angles[:-1], vals[:-1])):
                ax.annotate(f'{val:.0f}%', xy=(angle, val), fontsize=8, fontweight='bold', color='#C87961', ha='center', va='bottom')
            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            buf.seek(0)
            plt.close()
            return RLImage(buf, width=4*inch, height=4*inch)
        except Exception as e:
            print(f"Radar chart error: {e}")
            return None

    def _trait_detail_block(self, trait_key, score):
        """Generate Meaning + Expert Analysis + Development Plan for a single trait"""
        elements = []
        td = TRAIT_DATA.get(trait_key, {})
        label = td.get('label', trait_key.replace('_', ' ').title())
        band = self._get_band(score)
        band_data = td.get(band, td.get('Moderate', {}))

        # Trait header with score
        elements.append(Paragraph(f"<b>{label}</b> — Score: {score:.0f}% ({band})", self.styles['TraitHeading']))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E0E0E0'), spaceAfter=6))

        # Meaning
        meaning = td.get('meaning', '')
        if meaning:
            elements.append(Paragraph(f"<b>What it Means:</b> {meaning}", self.styles['ReportBody']))

        # Expert Analysis
        analysis = band_data.get('analysis', '')
        if analysis:
            elements.append(Paragraph(f"<b>Expert Analysis:</b> {analysis}", self.styles['ReportBody']))

        # Development Plan
        plan_str = band_data.get('plan', [''])[0] if band_data.get('plan') else ''
        if plan_str:
            elements.append(Paragraph("<b>Development Plan:</b>", self.styles['SmallLabel']))
            for tip in plan_str.split('|'):
                tip = tip.strip()
                if tip:
                    elements.append(Paragraph(f"\u2022 {tip}", self.styles['BulletItem']))

        elements.append(Spacer(1, 8))
        return elements

    def _dimension_section(self, title, intro_text, what_is_text, scores, trait_keys):
        """Build a complete dimension section: intro + chart + trait details"""
        elements = []
        elements.append(Paragraph(title, self.styles['SectionHeading']))

        # What is this dimension?
        elements.append(Paragraph(f"<b>What is {what_is_text}?</b>", self.styles['SubsectionHeading']))
        elements.append(Paragraph(intro_text, self.styles['ReportBody']))

        # Dominant traits
        sorted_traits = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_traits = sorted_traits[:3]
        dom_text = ", ".join([f"<b>{TRAIT_DATA.get(t, {}).get('label', t.replace('_',' ').title())}</b> ({s:.0f}%)" for t, s in top_traits])
        elements.append(Paragraph(f"Your Dominant Strengths: {dom_text}", self.styles['ReportBody']))
        elements.append(Spacer(1, 6))

        # Bar chart
        chart = self._create_bar_chart(scores, f"Your {what_is_text} Scores")
        if chart:
            elements.append(chart)
        elements.append(Spacer(1, 10))

        # Detailed trait analysis
        elements.append(Paragraph(f"Your {what_is_text} in Detail", self.styles['SubsectionHeading']))
        for tk in trait_keys:
            sc = scores.get(tk, 50)
            elements.extend(self._trait_detail_block(tk, sc))

        return elements

    # ============================================================
    # MAIN REPORT GENERATION
    # ============================================================
    def generate_report(self, user_data: Dict, test_results: List[Dict], report_id: str) -> str:
        filename = f"career_report_{report_id}.pdf"
        filepath = f"/tmp/{filename}"
        doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=45, bottomMargin=45,
                                title=f"Career Discovery Report - {user_data.get('full_name', 'Student')}")
        story = []

        # Collect all scores
        all_scores = {}
        for r in test_results:
            tt = r.get('test_type')
            all_scores[tt] = {'scores': r.get('scores', {}), 'details': r.get('scoring_details', {})}

        # 1. Cover Page
        story.extend(self._cover_page(user_data, report_id))
        story.append(PageBreak())

        # 2. Framework Introduction
        story.extend(self._framework_page())
        story.append(PageBreak())

        # 3. Executive Summary
        story.extend(self._executive_summary(all_scores))
        story.append(PageBreak())

        # 4-8. Dimension Sections
        dim_configs = [
            ('orientation', "Section 1: Work Orientation & Style Analysis",
             "Your work orientation reveals your natural preferences for different types of work environments and task approaches. Understanding your orientation style helps identify the kind of work settings where you will feel most energized, productive, and fulfilled. This dimension analyzes four key orientation styles that shape how you prefer to engage with your work.",
             "Orientation Style", ["creative", "analytical", "people_centric", "administrative"]),
            ('interest', "Section 2: Interest Mapping",
             "Your interests reflect what subjects, activities, and fields naturally attract your attention and curiosity. Strong interests in a domain indicate a higher likelihood of sustained motivation, deeper engagement, and long-term satisfaction in related careers. This dimension maps your interests across five broad career domains.",
             "Interest Profile", ["stem", "arts_humanities", "business_commerce", "healthcare", "social_service"]),
            ('personality', "Section 3: Personality Profile",
             "Your personality traits describe consistent patterns in how you think, feel, and behave across different situations. Understanding your personality helps predict how you will respond to workplace challenges, interact with colleagues, handle stress, and approach your career goals. This dimension analyzes eight key personality dimensions.",
             "Personality Profile", ["decision_making", "perseverance", "integrity", "leadership", "teamwork", "emotional_stability", "risk_appetite", "self_discipline"]),
            ('aptitude', "Section 4: Cognitive Aptitude Analysis",
             "Your cognitive aptitudes represent your natural abilities and potential in different types of mental tasks. Unlike knowledge (which is learned), aptitudes are innate strengths that indicate where you are likely to learn fastest and perform best. This dimension evaluates seven key cognitive aptitudes that influence career success.",
             "Aptitude Profile", ["verbal_reasoning", "numerical_ability", "logical_reasoning", "abstract_thinking", "spatial_visualization", "technological_understanding", "perceptual_speed"]),
            ('eq', "Section 5: Emotional Intelligence Profile",
             "Emotional Intelligence (EQ) is your ability to recognize, understand, manage, and effectively use emotions — both your own and those of others. Research consistently shows that EQ is a stronger predictor of career success and life satisfaction than IQ alone. This dimension analyzes six critical components of your emotional intelligence.",
             "Emotional Intelligence", ["emotional_awareness", "emotional_regulation", "empathy", "social_skills", "motivation", "conflict_management"]),
        ]

        for test_type, title, intro, what_is, traits in dim_configs:
            scores = all_scores.get(test_type, {}).get('scores', {})
            if scores:
                story.extend(self._dimension_section(title, intro, what_is, scores, traits))
                story.append(PageBreak())

        # 9. Career Recommendations
        story.extend(self._career_recommendations(all_scores))
        story.append(PageBreak())

        # 10. Strengths & Development Roadmap
        story.extend(self._strengths_roadmap(all_scores))
        story.append(PageBreak())

        # 11. Appendix
        story.extend(self._appendix())

        doc.build(story, onFirstPage=self._add_header_footer, onLaterPages=self._add_header_footer)
        return filepath

    def _cover_page(self, user_data, report_id):
        elements = []
        elements.append(Spacer(1, 1.2*inch))
        elements.append(Paragraph("Career Discovery Report", self.styles['ReportTitle']))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("Comprehensive Psychometric Assessment", ParagraphStyle('subtitle', parent=self.styles['Heading2'], alignment=TA_CENTER, textColor=colors.HexColor('#5D7A68'))))
        elements.append(Spacer(1, 0.5*inch))

        info_data = [
            ["Student Name", user_data.get('full_name', 'N/A')],
            ["Class", user_data.get('class_level', 'N/A')],
            ["School", user_data.get('school_name', 'N/A')],
            ["Report Date", datetime.now().strftime('%B %d, %Y')],
            ["Report ID", report_id[:16]],
        ]
        t = Table(info_data, colWidths=[2.5*inch, 3.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F0F4F8')),
            ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#FAFAFA')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1A2B4B')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.6*inch))

        elements.append(Paragraph(
            "This report presents a comprehensive analysis of your psychometric assessment across five scientific dimensions: "
            "Work Orientation, Interests, Personality, Cognitive Aptitude, and Emotional Intelligence. "
            "Each dimension is analyzed in depth with personalized expert insights and actionable development plans. "
            "Use this report to understand your unique strengths, discover suitable career paths, and chart your journey towards a fulfilling career.",
            self.styles['ReportBody']))
        elements.append(Spacer(1, 0.4*inch))

        elements.append(Paragraph(
            "<b>For Personalized Counselling:</b><br/>"
            "Shubham Raj Singh | Call/WhatsApp: 6200488068<br/>"
            "Email: shubhamrajsingh1712@gmail.com | www.BoatMyCareer.com",
            self.styles['SmallLabel']))
        return elements

    def _framework_page(self):
        elements = []
        elements.append(Paragraph("The BoatMyCareer Assessment Framework", self.styles['SectionHeading']))
        elements.append(Paragraph(
            "Our comprehensive psychometric assessment is built on a scientifically validated 5-dimensional framework "
            "that evaluates the key aspects of your personality, abilities, and preferences. Each dimension provides "
            "unique insights into your career potential, and together they paint a complete picture of who you are and "
            "where you are most likely to thrive.",
            self.styles['ReportBody']))
        elements.append(Spacer(1, 0.2*inch))

        dims = [
            ("1. Orientation Style", "Reveals your natural work preferences — whether you are drawn to creative innovation, systematic analysis, people interaction, or administrative organization."),
            ("2. Interest Profile", "Maps your curiosity and enthusiasm across five major career domains: STEM, Arts & Humanities, Business & Commerce, Healthcare, and Social Service."),
            ("3. Personality Profile", "Analyzes eight core personality dimensions including leadership, perseverance, integrity, decision-making, teamwork, emotional stability, risk appetite, and self-discipline."),
            ("4. Cognitive Aptitude", "Evaluates seven cognitive abilities: verbal reasoning, numerical ability, logical reasoning, abstract thinking, spatial visualization, technological understanding, and perceptual speed."),
            ("5. Emotional Intelligence", "Measures six components of emotional intelligence: self-awareness, emotional regulation, empathy, social skills, motivation, and conflict management."),
        ]
        for title, desc in dims:
            elements.append(Paragraph(f"<b>{title}</b>", self.styles['SubsectionHeading']))
            elements.append(Paragraph(desc, self.styles['ReportBody']))

        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph(
            "<b>How to Read This Report:</b> Each section presents your scores on a 0-100% scale, classified into three bands: "
            "<b>High (70-100%)</b> indicates a strong presence of the trait, "
            "<b>Moderate (40-69%)</b> indicates a balanced or developing level, and "
            "<b>Low (0-39%)</b> indicates an area for potential growth. "
            "Every trait includes a personalized expert analysis and an actionable development plan.",
            self.styles['ReportBody']))
        return elements

    def _executive_summary(self, all_scores):
        elements = []
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeading']))
        elements.append(Paragraph("Overall Profile Snapshot", self.styles['SubsectionHeading']))

        radar = self._create_radar_chart(all_scores)
        if radar:
            elements.append(radar)
            elements.append(Spacer(1, 0.15*inch))

        # Top strengths
        all_traits = []
        for tt, data in all_scores.items():
            for trait, sc in data.get('scores', {}).items():
                all_traits.append((trait, sc, tt))
        all_traits.sort(key=lambda x: x[1], reverse=True)

        elements.append(Paragraph("Key Strengths", self.styles['SubsectionHeading']))
        for trait, sc, dim in all_traits[:5]:
            label = TRAIT_DATA.get(trait, {}).get('label', trait.replace('_', ' ').title())
            elements.append(Paragraph(f"\u2022 <b>{label}</b> — {sc:.0f}% ({self._get_band(sc)}) [{dim.title()}]", self.styles['ReportBody']))

        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph("Key Development Areas", self.styles['SubsectionHeading']))
        for trait, sc, dim in all_traits[-3:]:
            label = TRAIT_DATA.get(trait, {}).get('label', trait.replace('_', ' ').title())
            elements.append(Paragraph(f"\u2022 <b>{label}</b> — {sc:.0f}% ({self._get_band(sc)}) [{dim.title()}]", self.styles['ReportBody']))

        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph("Quick Career Direction Indicators", self.styles['SubsectionHeading']))
        indicators = self._get_career_indicators(all_scores)
        for ind in indicators:
            elements.append(Paragraph(f"\u2022 {ind}", self.styles['ReportBody']))

        return elements

    def _get_career_indicators(self, all_scores):
        indicators = []
        o = all_scores.get('orientation', {}).get('scores', {})
        i = all_scores.get('interest', {}).get('scores', {})
        p = all_scores.get('personality', {}).get('scores', {})

        if o:
            dom = max(o, key=o.get)
            if dom == 'creative': indicators.append("Your creative orientation suggests careers in Design, Arts, Media, Architecture, or Creative Technology.")
            elif dom == 'analytical': indicators.append("Your analytical orientation suggests careers in Engineering, Data Science, Research, Finance, or Consulting.")
            elif dom == 'people_centric': indicators.append("Your people-centric orientation suggests careers in Education, Healthcare, HR, Counseling, or Social Work.")
            elif dom == 'administrative': indicators.append("Your administrative orientation suggests careers in Management, Banking, Government Services, or Operations.")

        if i:
            dom = max(i, key=i.get)
            if dom == 'stem': indicators.append("Your strong STEM interest aligns with Engineering, Technology, Medical Sciences, or Research careers.")
            elif dom == 'arts_humanities': indicators.append("Your Arts & Humanities interest aligns with Writing, Film, Fine Arts, Journalism, or Cultural Studies.")
            elif dom == 'business_commerce': indicators.append("Your Business interest aligns with Finance, Marketing, Entrepreneurship, or Management careers.")
            elif dom == 'healthcare': indicators.append("Your Healthcare interest aligns with Medicine, Pharmacy, Physiotherapy, or Public Health careers.")
            elif dom == 'social_service': indicators.append("Your Social Service interest aligns with Teaching, Social Work, NGO Management, or Community Development.")

        if p:
            if p.get('leadership', 0) > 70: indicators.append("Your strong leadership trait positions you well for managerial, entrepreneurial, and executive roles.")
            if p.get('integrity', 0) > 70: indicators.append("Your high integrity makes you suited for roles requiring trust: Law, Medicine, Civil Services, or Auditing.")
            if p.get('perseverance', 0) > 70: indicators.append("Your perseverance indicates success potential in demanding fields: Competitive Exams, Research, or Medicine.")

        if not indicators:
            indicators.append("Your balanced profile suggests versatile career options. Consider exploring multiple domains to find the best fit.")

        return indicators

    def _career_recommendations(self, all_scores):
        elements = []
        elements.append(Paragraph("Section 6: Career Recommendations", self.styles['SectionHeading']))
        elements.append(Paragraph(
            "Based on the comprehensive analysis of your orientation, interests, personality, aptitude, and emotional intelligence scores, "
            "the following career paths are recommended for your consideration. Each recommendation is matched to your unique profile.",
            self.styles['ReportBody']))
        elements.append(Spacer(1, 0.15*inch))

        # Determine top careers based on scores
        o = all_scores.get('orientation', {}).get('scores', {})
        i = all_scores.get('interest', {}).get('scores', {})
        top_o = max(o, key=o.get) if o else 'analytical'
        top_i = max(i, key=i.get) if i else 'stem'

        # Try to find a specific match
        key = f"high_{top_o}_high_{top_i}"
        careers = CAREER_MATCHES.get(key, CAREER_MATCHES.get('moderate_all', []))

        # Get career details from career_data
        try:
            from career_data import get_career_by_slug, get_categories
            import re
            cat_map = {c['id']: c['name'] for c in get_categories()}
        except Exception:
            cat_map = {}

        for idx, career_name in enumerate(careers[:5], 1):
            slug = re.sub(r'[^a-z0-9]+', '-', career_name.lower()).strip('-')
            try:
                career_detail = get_career_by_slug(slug)
            except Exception:
                career_detail = None

            elements.append(Paragraph(f"<b>Career Match #{idx}: {career_name}</b>", self.styles['SubsectionHeading']))

            if career_detail:
                elements.append(Paragraph(f"<b>Description:</b> {career_detail['description']}", self.styles['ReportBody']))
                elements.append(Paragraph(f"<b>Recommended Stream:</b> {career_detail['stream']}", self.styles['ReportBody']))
                elements.append(Paragraph(f"<b>Education:</b> {career_detail['education']['undergraduate']} → {career_detail['education']['postgraduate']}", self.styles['ReportBody']))
                elements.append(Paragraph(f"<b>Key Entrance Exams:</b> {', '.join(career_detail['entrance_exams'][:4])}", self.styles['ReportBody']))
                elements.append(Paragraph(f"<b>Top Institutions:</b> {', '.join(career_detail['top_institutions'][:4])}", self.styles['ReportBody']))
                sal = career_detail['salary']
                elements.append(Paragraph(f"<b>Salary Range:</b> Starting: {sal['starting']} | Mid-Career: {sal['mid_career']} | Senior: {sal['senior']}", self.styles['ReportBody']))
                elements.append(Paragraph(f"<b>Growth Outlook:</b> {career_detail['growth_outlook']}", self.styles['ReportBody']))
                elements.append(Paragraph(f"<b>Skills Required:</b> {', '.join(career_detail['skills_required'])}", self.styles['ReportBody']))
            else:
                elements.append(Paragraph(f"This career aligns well with your assessment profile. Please explore our Career Library at www.BoatMyCareer.com/careers for detailed information.", self.styles['ReportBody']))

            elements.append(Spacer(1, 10))
            elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E0E0E0'), spaceAfter=8))

        return elements

    def _strengths_roadmap(self, all_scores):
        elements = []
        elements.append(Paragraph("Section 7: Strengths & Development Roadmap", self.styles['SectionHeading']))

        all_traits = []
        for tt, data in all_scores.items():
            for trait, sc in data.get('scores', {}).items():
                all_traits.append((trait, sc, tt))
        all_traits.sort(key=lambda x: x[1], reverse=True)

        # Top 5 strengths
        elements.append(Paragraph("Your Top Strengths", self.styles['SubsectionHeading']))
        elements.append(Paragraph("These are the areas where you naturally excel. Leverage these strengths in your career choice and daily activities.", self.styles['ReportBody']))
        for trait, sc, dim in all_traits[:5]:
            label = TRAIT_DATA.get(trait, {}).get('label', trait.replace('_', ' ').title())
            elements.append(Paragraph(f"\u2022 <b>{label}</b> ({sc:.0f}%) — This strength positions you well for roles requiring {label.lower()} across {dim.replace('_', ' ').title()} domains.", self.styles['ReportBody']))

        elements.append(Spacer(1, 0.15*inch))

        # Development areas
        elements.append(Paragraph("Priority Development Areas", self.styles['SubsectionHeading']))
        elements.append(Paragraph("Focused development in these areas will significantly enhance your overall career readiness.", self.styles['ReportBody']))
        for trait, sc, dim in all_traits[-5:]:
            label = TRAIT_DATA.get(trait, {}).get('label', trait.replace('_', ' ').title())
            band = self._get_band(sc)
            td = TRAIT_DATA.get(trait, {})
            plan_str = td.get(band, {}).get('plan', [''])[0] if td.get(band) else ''
            first_tip = plan_str.split('|')[0].strip() if plan_str else 'Work on developing this area gradually.'
            elements.append(Paragraph(f"\u2022 <b>{label}</b> ({sc:.0f}%) — {first_tip}", self.styles['ReportBody']))

        elements.append(Spacer(1, 0.15*inch))

        # Action plan summary
        elements.append(Paragraph("Your 90-Day Action Plan", self.styles['SubsectionHeading']))
        elements.append(Paragraph("\u2022 <b>Month 1 (Explore):</b> Research the top 3 career recommendations in this report. Visit www.BoatMyCareer.com/careers for detailed career information. Talk to professionals in these fields.", self.styles['ReportBody']))
        elements.append(Paragraph("\u2022 <b>Month 2 (Develop):</b> Start working on your top 2 development areas using the specific plans provided in this report. Join at least one relevant extracurricular activity.", self.styles['ReportBody']))
        elements.append(Paragraph("\u2022 <b>Month 3 (Plan):</b> Schedule a one-on-one counselling session with BoatMyCareer to create a detailed academic and career roadmap. Begin preparing for relevant entrance exams.", self.styles['ReportBody']))

        return elements

    def _appendix(self):
        elements = []
        elements.append(Paragraph("Appendix", self.styles['SectionHeading']))
        elements.append(Paragraph("Score Band Reference", self.styles['SubsectionHeading']))

        band_data = [
            ["Band", "Score Range", "Interpretation"],
            ["High", "70 - 100%", "Strong presence of the trait. A natural strength to be leveraged."],
            ["Moderate", "40 - 69%", "Balanced or developing level. Can be strengthened with conscious effort."],
            ["Low", "0 - 39%", "Area for growth. Specific development strategies can help improve this area."],
        ]
        bt = Table(band_data, colWidths=[1.2*inch, 1.5*inch, 3.5*inch])
        bt.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A2B4B')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FAFAFA')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(bt)
        elements.append(Spacer(1, 0.3*inch))

        elements.append(Paragraph("Important Disclaimer", self.styles['SubsectionHeading']))
        elements.append(Paragraph(
            "This psychometric assessment report is a scientifically designed guidance tool to help you understand your strengths, "
            "interests, and potential career directions. It is NOT a deterministic prediction of your future success or a clinical diagnosis. "
            "Career decisions should be made in consultation with parents, educators, and professional counselors, considering multiple factors "
            "including personal interests, academic performance, family circumstances, and market opportunities.",
            self.styles['ReportBody']))
        elements.append(Paragraph(
            "The assessment results represent your responses at a specific point in time and may evolve as you grow and gain more experiences. "
            "We recommend combining these insights with practical exploration, internships, and personalized career counseling for the best outcomes.",
            self.styles['ReportBody']))
        elements.append(Spacer(1, 0.15*inch))
        elements.append(Paragraph("<b>Final decisions regarding your career path rest with you and your family.</b>", self.styles['ReportBody']))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph(
            "<b>About BoatMyCareer.com</b><br/>"
            "Founded by Shubham Raj Singh, BoatMyCareer.com is dedicated to providing scientific, personalized career guidance "
            "to students in Class VII to XII. Our 5-stage program combines psychometric assessment, expert counseling, and continuous "
            "guidance to help every student discover and pursue their ideal career path.<br/><br/>"
            "<b>Contact Us:</b> Call/WhatsApp: 6200488068 | Email: shubhamrajsingh1712@gmail.com | Web: www.BoatMyCareer.com",
            self.styles['ReportBody']))

        return elements

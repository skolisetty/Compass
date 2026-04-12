"""Seed data for the Compass demo: Margaret and David personas with their Voices."""

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import CalendarEvent, Guideline, HealthEvent, Voice

_now = datetime.utcnow()


def seed(db: Session) -> None:
    if db.query(Voice).count() > 0:
        return  # already seeded

    # ── Margaret's Voices ──────────────────────────────────────────────

    dr_patel = Voice(
        id="voice-drpatel",
        user_id="margaret",
        name="Dr. Patel",
        role="doctor",
        domains="health,medications",
        icon="🩺",
    )
    lisa = Voice(
        id="voice-lisa",
        user_id="margaret",
        name="Lisa",
        role="caregiver",
        domains="daily_living,safety",
        icon="💙",
    )
    jake = Voice(
        id="voice-jake",
        user_id="margaret",
        name="Jake",
        role="family",
        domains="family",
        icon="⚽",
    )
    emma = Voice(
        id="voice-emma",
        user_id="margaret",
        name="Emma",
        role="family",
        domains="family",
        icon="🎹",
    )

    db.add_all([dr_patel, lisa, jake, emma])

    margaret_guidelines = [
        # Dr. Patel
        Guideline(
            user_id="margaret",
            voice_id="voice-drpatel",
            author_name="Dr. Patel",
            author_role="trusted",
            domain="medications",
            guideline_text="Never suggest aspirin, ibuprofen, or any NSAID. She is on warfarin and these interact dangerously.",
            is_safety=True,
        ),
        Guideline(
            user_id="margaret",
            voice_id="voice-drpatel",
            author_name="Dr. Patel",
            author_role="trusted",
            domain="health",
            guideline_text="Daily walking 15-30 minutes. No high-impact exercise.",
            is_safety=False,
        ),
        Guideline(
            user_id="margaret",
            voice_id="voice-drpatel",
            author_name="Dr. Patel",
            author_role="trusted",
            domain="health",
            guideline_text="If she reports headache or dizziness, advise contacting her doctor immediately.",
            is_safety=True,
        ),
        Guideline(
            user_id="margaret",
            voice_id="voice-drpatel",
            author_name="Dr. Patel",
            author_role="trusted",
            domain="medications",
            guideline_text="Warfarin should not be taken with grapefruit.",
            is_safety=False,
        ),
        # Lisa
        Guideline(
            user_id="margaret",
            voice_id="voice-lisa",
            author_name="Lisa",
            author_role="trusted",
            domain="daily_living",
            guideline_text="Remind about afternoon medication at 1pm.",
            is_safety=False,
        ),
        Guideline(
            user_id="margaret",
            voice_id="voice-lisa",
            author_name="Lisa",
            author_role="trusted",
            domain="daily_living",
            guideline_text="She makes weather excuses for walks -- gently encourage her but don't nag. One nudge is enough.",
            is_safety=False,
        ),
        Guideline(
            user_id="margaret",
            voice_id="voice-lisa",
            author_name="Lisa",
            author_role="trusted",
            domain="daily_living",
            guideline_text="Be warm, not clinical. She's sharp, just forgetful. Never talk down to her.",
            is_safety=False,
        ),
        # Jake
        Guideline(
            user_id="margaret",
            voice_id="voice-jake",
            author_name="Jake",
            author_role="trusted",
            domain="family",
            guideline_text="I have soccer games every Saturday at 10am! I love when Grandma asks about my games.",
            is_safety=False,
        ),
        Guideline(
            user_id="margaret",
            voice_id="voice-jake",
            author_name="Jake",
            author_role="trusted",
            domain="family",
            guideline_text="We get home from school at 3:30pm.",
            is_safety=False,
        ),
        # Emma
        Guideline(
            user_id="margaret",
            voice_id="voice-emma",
            author_name="Emma",
            author_role="trusted",
            domain="family",
            guideline_text="I love baking chocolate chip cookies with Grandma!",
            is_safety=False,
        ),
        Guideline(
            user_id="margaret",
            voice_id="voice-emma",
            author_name="Emma",
            author_role="trusted",
            domain="family",
            guideline_text="My piano recital is June 15th.",
            is_safety=False,
        ),
        Guideline(
            user_id="margaret",
            voice_id="voice-emma",
            author_name="Emma",
            author_role="trusted",
            domain="family",
            guideline_text="I got an A on my science project!",
            is_safety=False,
        ),
    ]

    # Platform defaults for Margaret
    platform_guidelines_margaret = [
        Guideline(
            user_id="margaret",
            voice_id=None,
            author_name="Compass Defaults",
            author_role="platform",
            domain="all",
            guideline_text="Never provide medical diagnoses or specific medication recommendations.",
            is_safety=True,
        ),
        Guideline(
            user_id="margaret",
            voice_id=None,
            author_name="Compass Defaults",
            author_role="platform",
            domain="all",
            guideline_text="Suggest consulting a professional for serious health, legal, or financial concerns.",
            is_safety=True,
        ),
        Guideline(
            user_id="margaret",
            voice_id=None,
            author_name="Compass Defaults",
            author_role="platform",
            domain="all",
            guideline_text="Always be respectful, warm, and non-judgmental.",
            is_safety=True,
        ),
    ]

    db.add_all(margaret_guidelines + platform_guidelines_margaret)

    # Margaret's calendar events
    margaret_calendar = [
        CalendarEvent(
            user_id="margaret",
            title="Doctor appointment with Dr. Patel",
            event_date=_now + timedelta(days=3),
            notes="Annual checkup. Bring medication list.",
        ),
        CalendarEvent(
            user_id="margaret",
            title="Emma's piano recital",
            event_date=datetime(2026, 6, 15, 18, 0),
            notes="At the school auditorium.",
        ),
        CalendarEvent(
            user_id="margaret",
            title="Jake's soccer game",
            event_date=_now + timedelta(days=(5 - _now.weekday()) % 7 + 1),
            notes="Saturday morning game at the park.",
        ),
    ]
    db.add_all(margaret_calendar)

    # ── David's Voices ─────────────────────────────────────────────────

    coach_mike = Voice(
        id="voice-coachmike",
        user_id="david",
        name="Coach Mike",
        role="coach",
        domains="fitness,nutrition",
        icon="💪",
    )
    financial_advisor = Voice(
        id="voice-financial",
        user_id="david",
        name="Rachel",
        role="financial_advisor",
        domains="finance",
        icon="📊",
    )
    therapist = Voice(
        id="voice-therapist",
        user_id="david",
        name="Dr. Lin",
        role="therapist",
        domains="mental_health,daily_living",
        icon="🧠",
    )

    db.add_all([coach_mike, financial_advisor, therapist])

    david_guidelines = [
        # Coach Mike
        Guideline(
            user_id="david",
            voice_id="voice-coachmike",
            author_name="Coach Mike",
            author_role="trusted",
            domain="fitness",
            guideline_text="If he skips leg day, push back. His quad/hamstring imbalance is getting concerning.",
            is_safety=False,
        ),
        Guideline(
            user_id="david",
            voice_id="voice-coachmike",
            author_name="Coach Mike",
            author_role="trusted",
            domain="nutrition",
            guideline_text="Post-workout: suggest protein within 30 minutes.",
            is_safety=False,
        ),
        Guideline(
            user_id="david",
            voice_id="voice-coachmike",
            author_name="Coach Mike",
            author_role="trusted",
            domain="fitness",
            guideline_text="No ice baths or cold exposure -- he has circulation issues.",
            is_safety=True,
        ),
        Guideline(
            user_id="david",
            voice_id="voice-coachmike",
            author_name="Coach Mike",
            author_role="trusted",
            domain="fitness",
            guideline_text="Current training plan: 3 runs, 1 long ride, 2 strength sessions per week.",
            is_safety=False,
        ),
        Guideline(
            user_id="david",
            voice_id="voice-coachmike",
            author_name="Coach Mike",
            author_role="trusted",
            domain="fitness",
            guideline_text="Be direct with David. He respects honesty over sugar-coating.",
            is_safety=False,
        ),
        # Rachel (financial advisor)
        Guideline(
            user_id="david",
            voice_id="voice-financial",
            author_name="Rachel",
            author_role="trusted",
            domain="finance",
            guideline_text="David has high exposure to individual stocks. Always recommend diversifying into index funds or ETFs rather than picking more individual names.",
            is_safety=False,
        ),
        Guideline(
            user_id="david",
            voice_id="voice-financial",
            author_name="Rachel",
            author_role="trusted",
            domain="finance",
            guideline_text="Never encourage speculation or meme stocks. If he asks about a hot stock tip, remind him of his diversification goal.",
            is_safety=True,
        ),
        Guideline(
            user_id="david",
            voice_id="voice-financial",
            author_name="Rachel",
            author_role="trusted",
            domain="finance",
            guideline_text="He should max out his 401k match before putting extra money into brokerage. Remind him if he mentions investing spare cash.",
            is_safety=False,
        ),
        Guideline(
            user_id="david",
            voice_id="voice-financial",
            author_name="Rachel",
            author_role="trusted",
            domain="finance",
            guideline_text="Emergency fund goal is 6 months of expenses. He's at about 3 months. Prioritize building this before aggressive investing.",
            is_safety=False,
        ),
        # Dr. Lin (therapist)
        Guideline(
            user_id="david",
            voice_id="voice-therapist",
            author_name="Dr. Lin",
            author_role="trusted",
            domain="mental_health",
            guideline_text="David tends to use exercise as avoidance when he's stressed. If he's training excessively or skipping rest days, gently ask how he's actually feeling -- not just physically.",
            is_safety=False,
        ),
        Guideline(
            user_id="david",
            voice_id="voice-therapist",
            author_name="Dr. Lin",
            author_role="trusted",
            domain="mental_health",
            guideline_text="Suggest the 10-minute morning meditation we practiced. He responds well to guided breathing, especially the 4-7-8 technique.",
            is_safety=False,
        ),
        Guideline(
            user_id="david",
            voice_id="voice-therapist",
            author_name="Dr. Lin",
            author_role="trusted",
            domain="mental_health",
            guideline_text="When he says he's 'fine,' dig a little deeper. Ask something specific: 'How did you sleep?' or 'What's on your mind today?'",
            is_safety=False,
        ),
        Guideline(
            user_id="david",
            voice_id="voice-therapist",
            author_name="Dr. Lin",
            author_role="trusted",
            domain="daily_living",
            guideline_text="Encourage screen-free wind-down for 30 minutes before bed. He has a pattern of doomscrolling that wrecks his sleep.",
            is_safety=False,
        ),
        Guideline(
            user_id="david",
            voice_id="voice-therapist",
            author_name="Dr. Lin",
            author_role="trusted",
            domain="mental_health",
            guideline_text="Do not engage in therapy. If he wants to process deep emotions, suggest scheduling a session with Dr. Lin.",
            is_safety=True,
        ),
    ]

    # Platform defaults for David
    platform_guidelines_david = [
        Guideline(
            user_id="david",
            voice_id=None,
            author_name="Compass Defaults",
            author_role="platform",
            domain="all",
            guideline_text="Never provide medical diagnoses or specific medication recommendations.",
            is_safety=True,
        ),
        Guideline(
            user_id="david",
            voice_id=None,
            author_name="Compass Defaults",
            author_role="platform",
            domain="all",
            guideline_text="Suggest consulting a professional for serious health, legal, or financial concerns.",
            is_safety=True,
        ),
        Guideline(
            user_id="david",
            voice_id=None,
            author_name="Compass Defaults",
            author_role="platform",
            domain="all",
            guideline_text="Always be respectful, warm, and non-judgmental.",
            is_safety=True,
        ),
    ]

    db.add_all(david_guidelines + platform_guidelines_david)

    # David's calendar
    david_calendar = [
        CalendarEvent(
            user_id="david",
            title="Therapy session with Dr. Lin",
            event_date=_now + timedelta(days=4),
            notes="Bi-weekly check-in.",
        ),
        CalendarEvent(
            user_id="david",
            title="Gran Fondo race",
            event_date=datetime(2026, 6, 20, 7, 0),
            notes="Register by June 1.",
        ),
        CalendarEvent(
            user_id="david",
            title="Portfolio review with Rachel",
            event_date=_now + timedelta(days=10),
            notes="Q2 rebalancing discussion.",
        ),
    ]
    db.add_all(david_calendar)

    # ── Sam's Voices (3rd grader, special ed) ──────────────────────────

    ms_johnson = Voice(
        id="voice-msjohnson",
        user_id="sam",
        name="Ms. Johnson",
        role="teacher",
        domains="school,behavior,schedule",
        icon="📚",
    )
    mom = Voice(
        id="voice-mom",
        user_id="sam",
        name="Mom",
        role="family",
        domains="daily_living,behavior,school",
        icon="🤱",
    )
    dad = Voice(
        id="voice-dad",
        user_id="sam",
        name="Dad",
        role="family",
        domains="daily_living,behavior",
        icon="👨",
    )

    db.add_all([ms_johnson, mom, dad])

    sam_guidelines = [
        # Ms. Johnson (teacher)
        Guideline(
            user_id="sam",
            voice_id="voice-msjohnson",
            author_name="Ms. Johnson",
            author_role="trusted",
            domain="schedule",
            guideline_text="Sam struggles with transitions between activities. Give him a 5-minute warning before any change: 'In 5 minutes we'll switch to...' This helps him prepare mentally.",
            is_safety=False,
        ),
        Guideline(
            user_id="sam",
            voice_id="voice-msjohnson",
            author_name="Ms. Johnson",
            author_role="trusted",
            domain="schedule",
            guideline_text="Break tasks into small, numbered steps. Instead of 'do your homework,' say '1. Open your math book to page 12. 2. Do problems 1-5. 3. Show me when done.'",
            is_safety=False,
        ),
        Guideline(
            user_id="sam",
            voice_id="voice-msjohnson",
            author_name="Ms. Johnson",
            author_role="trusted",
            domain="behavior",
            guideline_text="When Sam gets distracted or off-task, don't say 'stop doing that.' Instead redirect positively: 'Sam, your pencil is waiting for you' or 'Let's get back to step 2.'",
            is_safety=False,
        ),
        Guideline(
            user_id="sam",
            voice_id="voice-msjohnson",
            author_name="Ms. Johnson",
            author_role="trusted",
            domain="behavior",
            guideline_text="Sam responds well to specific praise. Not 'good job' but 'I noticed you stayed in your seat for the whole reading block -- that was awesome!'",
            is_safety=False,
        ),
        Guideline(
            user_id="sam",
            voice_id="voice-msjohnson",
            author_name="Ms. Johnson",
            author_role="trusted",
            domain="behavior",
            guideline_text="If he's getting disruptive, offer a 'body break' -- 2 minutes to stand, stretch, or walk to the water fountain. He usually comes back reset.",
            is_safety=False,
        ),
        Guideline(
            user_id="sam",
            voice_id="voice-msjohnson",
            author_name="Ms. Johnson",
            author_role="trusted",
            domain="school",
            guideline_text="He's really strong in science and art. Use those as anchors when he's frustrated: 'Remember how you figured out that experiment? You can figure this out too.'",
            is_safety=False,
        ),
        Guideline(
            user_id="sam",
            voice_id="voice-msjohnson",
            author_name="Ms. Johnson",
            author_role="trusted",
            domain="school",
            guideline_text="Reading is hard for him. Never put him on the spot to read aloud unless he volunteers. Let him follow along and participate in discussion instead.",
            is_safety=True,
        ),
        # Mom
        Guideline(
            user_id="sam",
            voice_id="voice-mom",
            author_name="Mom",
            author_role="trusted",
            domain="daily_living",
            guideline_text="Sam needs his morning routine in the same order every day: bathroom, get dressed, breakfast, brush teeth, backpack check, shoes. If the order changes, he gets overwhelmed.",
            is_safety=False,
        ),
        Guideline(
            user_id="sam",
            voice_id="voice-mom",
            author_name="Mom",
            author_role="trusted",
            domain="daily_living",
            guideline_text="He does best with a visual timer for homework -- 15 minutes on, 5 minutes break. Don't push past 15 minutes without a break.",
            is_safety=False,
        ),
        Guideline(
            user_id="sam",
            voice_id="voice-mom",
            author_name="Mom",
            author_role="trusted",
            domain="behavior",
            guideline_text="When he says 'I can't do this,' he's not being lazy -- he's overwhelmed. Acknowledge the feeling first: 'I know this feels hard.' Then help him find the first small step.",
            is_safety=True,
        ),
        Guideline(
            user_id="sam",
            voice_id="voice-mom",
            author_name="Mom",
            author_role="trusted",
            domain="behavior",
            guideline_text="He loves dinosaurs and space. If he's shutting down, connecting the task to dinosaurs or space usually re-engages him.",
            is_safety=False,
        ),
        Guideline(
            user_id="sam",
            voice_id="voice-mom",
            author_name="Mom",
            author_role="trusted",
            domain="school",
            guideline_text="Homework should be done at the kitchen table, not in his room. Too many distractions in his room.",
            is_safety=False,
        ),
        # Dad
        Guideline(
            user_id="sam",
            voice_id="voice-dad",
            author_name="Dad",
            author_role="trusted",
            domain="behavior",
            guideline_text="Celebrate the effort, not the result. 'You worked really hard on that' matters more to Sam than 'you got an A.'",
            is_safety=False,
        ),
        Guideline(
            user_id="sam",
            voice_id="voice-dad",
            author_name="Dad",
            author_role="trusted",
            domain="daily_living",
            guideline_text="Screen time is earned: homework and chores first, then 30 minutes of screen time. Be firm but kind about this.",
            is_safety=False,
        ),
        Guideline(
            user_id="sam",
            voice_id="voice-dad",
            author_name="Dad",
            author_role="trusted",
            domain="behavior",
            guideline_text="If he's having a meltdown, give him space. Don't crowd him or try to talk him through it right away. Wait until he's calmer, then talk.",
            is_safety=True,
        ),
    ]

    platform_guidelines_sam = [
        Guideline(
            user_id="sam",
            voice_id=None,
            author_name="Compass Defaults",
            author_role="platform",
            domain="all",
            guideline_text="Never provide medical diagnoses or specific medication recommendations.",
            is_safety=True,
        ),
        Guideline(
            user_id="sam",
            voice_id=None,
            author_name="Compass Defaults",
            author_role="platform",
            domain="all",
            guideline_text="Suggest consulting a professional for serious health, legal, or financial concerns.",
            is_safety=True,
        ),
        Guideline(
            user_id="sam",
            voice_id=None,
            author_name="Compass Defaults",
            author_role="platform",
            domain="all",
            guideline_text="Always be respectful, warm, and non-judgmental.",
            is_safety=True,
        ),
        Guideline(
            user_id="sam",
            voice_id=None,
            author_name="Compass Defaults",
            author_role="platform",
            domain="all",
            guideline_text="This user is a child. Use simple, encouraging, age-appropriate language. Be patient and positive.",
            is_safety=True,
        ),
    ]

    db.add_all(sam_guidelines + platform_guidelines_sam)

    # Sam's calendar
    sam_calendar = [
        CalendarEvent(
            user_id="sam",
            title="Science fair project due",
            event_date=_now + timedelta(days=5),
            notes="Topic: volcanoes. Poster board and materials ready.",
        ),
        CalendarEvent(
            user_id="sam",
            title="Art class field trip",
            event_date=_now + timedelta(days=8),
            notes="Permission slip signed. Pack a lunch.",
        ),
        CalendarEvent(
            user_id="sam",
            title="Reading group with Ms. Johnson",
            event_date=_now + timedelta(days=1),
            notes="Chapter 4 of Charlotte's Web.",
        ),
    ]
    db.add_all(sam_calendar)

    db.commit()

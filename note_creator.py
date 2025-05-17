import uuid
from aqt import mw
from anki.models import NotetypeDict
from anki.notes import Note
from aqt.utils import showInfo

def create_note_type() -> NotetypeDict:
    mm = mw.col.models
    model = mm.by_name("Chess Move from PGN")
    
    fields = ["UID", "Title", "Current_Position", "Last_Move", "Last_Move_Coordinate", 
              "Next_Move_Position", "Next_Move", "Next_Move_Coordinate", "Next_Move_Comment",
              "Site", "Date", "White", "Black", "Is_Black"]
    
    if model:
        # Check for missing fields and add them
        existing_fields = [f['name'] for f in model['flds']]
        for field in fields:
            if field not in existing_fields:
                mm.add_field(model, mm.new_field(field))
        mm.save(model)
    else:
        # Create new model if it doesn't exist
        model = mm.new("Chess Move from PGN")
        
        for field in fields:
            mm.add_field(model, mm.new_field(field))

        # Add card template
        t = mm.new_template("Chess Move")
        t['qfmt'] = "{{Title}}\n{{Current_Position}}\n{{Last_Move}}"
        t['afmt'] = "{{FrontSide}}<hr id=answer>{{Next_Move}}{{#Next_Move_Comment}}<br>{{Next_Move_Comment}}{{/Next_Move_Comment}}"
        mm.add_template(model, t)

        mm.add(model)
    
    return model

def create_notes_from_pgn(pgn_text: str, custom_title: str, is_black: bool) -> None:
    debug_info = "Starting note creation...\n"
    try:
        from .pgn_parser import parse_pgn
        parsed_pgn = parse_pgn(pgn_text)
        
        model = create_note_type()

        deck_id = mw.col.decks.id("Chess Moves from PGN")
        
        debug_info += f"Creating notes for {len(parsed_pgn['position_pairs'])} positions...\n"
        for i, pair in enumerate(parsed_pgn['position_pairs'], 1):
            note = Note(mw.col, model)
            
            note['UID'] = str(uuid.uuid4())
            note['Title'] = custom_title
            note['Current_Position'] = pair.get('current_fen', '')
            note['Last_Move'] = pair.get('last_move', '') or ''
            note['Last_Move_Coordinate'] = pair.get('last_move_uci', '') or ''
            note['Next_Move_Position'] = pair.get('next_fen', '')
            note['Next_Move'] = pair.get('next_move', '')
            note['Next_Move_Coordinate'] = pair.get('next_move_uci', '')
            note['Next_Move_Comment'] = pair.get('comment', '')           
            note['Site'] = parsed_pgn['header'].get('Site', '')
            note['Date'] = parsed_pgn['header'].get('Date', '')
            note['White'] = parsed_pgn['header'].get('White', '')
            note['Black'] = parsed_pgn['header'].get('Black', '')
            note['Is_Black'] = 'true' if is_black else ''

            note.add_tag('chess')
            note.add_tag('chess-moves-from-PGN')
            
            mw.col.add_note(note, deck_id)
            debug_info += f"Created note {i}: {note['Last_Move']} -> {note['Next_Move']}\n"

        mw.col.save()
        
        debug_info += f"\nCreated {len(parsed_pgn['position_pairs'])} notes from the PGN."
        showInfo(debug_info)
    except Exception as e:
        error_msg = f"Error creating notes: {str(e)}\n\nDebug info:\n{debug_info}"
        showInfo(error_msg)
        raise
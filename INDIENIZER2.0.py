import tkinter as tk
from tkinter import ttk, scrolledtext
import os

# Colors and font (Ableton-inspired, pastel)
BG_COLOR = "#23272A"
FRAME_COLOR = "#181A1B"
ACCENT_BLUE = "#EAF7FF"    
ACCENT_GREY = "#5B7C96"   
BTN_COLOR = "#5B7C96"
BTN_HOVER = ACCENT_GREY
TEXT_COLOR = "#FFFFFF"
BORDER_COLOR = "#35383A"
FONT = ("Arial Rounded MT", 11)
TITLE_FONT = ("Arial Rounded MT", 18, "bold")
LOGO_FONT = ("Arial Rounded MT", 30, "bold")
SCALE_TITLE_FONT = ("Arial Rounded MT", 12, "bold")
SCALE_NOTES_FONT = ("Arial Rounded MT", 11)
CHORD_TITLE_FONT = ("Arial Rounded MT", 12, "bold")
CHORD_NOTES_FONT = ("Arial Rounded MT", 11)
ADAPT_TITLE_FONT = ("Arial Rounded MT", 12, "bold")
ADAPT_NOTES_FONT = ("Arial Rounded MT", 11)
SEPARATOR_COLOR = "#23272A" # Darker for separation lines

notes_list = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
note_to_index_map = {note: index for index, note in enumerate(notes_list)}

# Scale patterns defined by intervals (semitones)
scale_patterns = {
    "major":            [2, 2, 1, 2, 2, 2, 1],
    "natural_minor":    [2, 1, 2, 2, 1, 2, 2],
    "harmonic_minor":   [2, 1, 2, 2, 1, 3, 1],
    "melodic_minor_asc":[2, 1, 2, 2, 2, 2, 1],
    "melodic_minor_desc":[2, 2, 1, 2, 2, 1, 2], # Same as major descending
    "major_pentatonic": [2, 2, 3, 2, 3],
    "minor_pentatonic": [3, 2, 2, 3, 2],
    "blues":            [3, 2, 1, 1, 3, 2],
    "whole_tone":       [2, 2, 2, 2, 2, 2],
    "octatonic":        [2, 1, 2, 1, 2, 1, 2, 1],
    "ionian":           [2, 2, 1, 2, 2, 2, 1],
    "dorian":           [2, 1, 2, 2, 2, 1, 2],
    "phrygian":         [1, 2, 2, 2, 1, 2, 2],
    "lydian":           [2, 2, 2, 1, 2, 2, 1],
    "mixolydian":       [2, 2, 1, 2, 2, 1, 2],
    "aeolian":          [2, 1, 2, 2, 1, 2, 2],
    "locrian":          [1, 2, 2, 1, 2, 2, 2],
}

# --- MODIFIED --- Chord types now distinguish 'dom' (dominant 7th) chords
# This is crucial for assigning correct extensions like '7', '9', '7alt'
chord_types_map = {
    "major":            ['maj', 'min', 'min', 'maj', 'dom', 'min', 'dim'],
    "ionian":           ['maj', 'min', 'min', 'maj', 'dom', 'min', 'dim'],
    "natural_minor":    ['min', 'dim', 'maj', 'min', 'min', 'maj', 'maj'],
    "aeolian":          ['min', 'dim', 'maj', 'min', 'min', 'maj', 'maj'],
    "harmonic_minor":   ['min', 'dim', 'aug', 'min', 'dom', 'maj', 'dim'],
    "melodic_minor_asc":['min', 'min', 'aug', 'dom', 'dom', 'dim', 'dim'],
    "melodic_minor_desc":['min', 'dim', 'maj', 'min', 'min', 'maj', 'maj'],
    "dorian":           ['min', 'min', 'maj', 'dom', 'min', 'dim', 'maj'],
    "phrygian":         ['min', 'maj', 'dom', 'min', 'dim', 'maj', 'min'],
    "lydian":           ['maj', 'dom', 'min', 'dim', 'maj', 'min', 'min'],
    "mixolydian":       ['dom', 'min', 'dim', 'maj', 'min', 'min', 'maj'],
    "locrian":          ['dim', 'maj', 'min', 'min', 'maj', 'dom', 'min'],
}

# --- UPDATED --- Extension compatibility with proper major/minor distinction
extension_compatibility = {
    'maj': ['maj7', 'maj9', '6', 'add9', 'sus2', 'sus4', 'add11', '#11', '13'],
    'min': ['m7', 'm9', 'm11', 'm6', 'madd9', 'sus2', 'sus4', 'madd11'],
    'dom': ['7', '9', '11', '13', '7sus4', '7b9', '7#9', '7#11', '7b13', '7alt', 'sus4'],
    'dim': ['dim7', 'm7b5'],
    'aug': ['maj7#5', '+7']
}

# Scales associated with each artist style
style_scales = {
    "EMPTY": [],
    "Phoebe Bridgers": ["aeolian", "dorian", "mixolydian"],
    "Angus & Julia Stone": ["aeolian", "dorian", "major_pentatonic"],
    "Low Roar": ["aeolian", "dorian", "minor_pentatonic"],
    "Novo Amor": ["aeolian", "dorian", "major_pentatonic"],
    "SYML": ["aeolian", "harmonic_minor", "dorian"],
    "Iron & Wine": ["aeolian", "mixolydian", "major_pentatonic"],
    "Bon Iver": ["dorian", "aeolian", "lydian", "mixolydian"], # Added more for variety
    "Leif Vollebekk": ["dorian", "mixolydian", "minor_pentatonic"],
    "Lana Del Rey": ["harmonic_minor", "aeolian", "dorian"],
    "Alexandra Savior": ["aeolian", "harmonic_minor", "phrygian"],
    "London Grammar": ["dorian", "aeolian", "harmonic_minor"],
    "Billie Eilish": ["phrygian", "harmonic_minor", "blues"],
}

# --- UPDATED --- Artist extensions with proper major/minor notation
artist_extensions_data = {
    "EMPTY": [],
    "Phoebe Bridgers": ["maj7", "m7", "sus2", "sus4", "add9", "madd9"],
    "Angus & Julia Stone": ["maj7", "m7", "sus2", "sus4", "add9", "madd9", "add11", "madd11"],
    "Low Roar": ["maj7", "m7", "sus2", "sus4", "add9", "madd9"],
    "Novo Amor": ["maj7", "m7", "sus2", "sus4", "add9", "madd9"],
    "SYML": ["maj7", "m7", "sus2", "sus4", "add9", "madd9"],
    "Iron & Wine": ["maj7", "m7", "sus2", "sus4", "add9", "madd9"],
    "Bon Iver": ["maj7", "m7", "maj9", "m9", "sus2", "sus4", "add9", "madd9", "m7b5", "7#11", "7b13", "7alt", "7"],
    "Leif Vollebekk": ["maj7", "m7", "sus2", "sus4", "add9", "madd9", "7"],
    "Lana Del Rey": ["maj7", "m7", "dim7", "sus4", "add9", "madd9", "6", "m6", "7"],
    "Alexandra Savior": ["maj7", "m7", "sus2", "sus4", "add9", "madd9", "dim7"],
    "London Grammar": ["maj7", "m7", "m9", "sus2", "sus4", "add9", "madd9", "add11", "madd11"],
    "Billie Eilish": ["m7", "maj7", "dim7", "m7b5", "sus2", "add9", "madd9", "7"]
}

# Borrowed chords are described per key type (major/minor)
artist_borrowed_chords_data = {
    "Phoebe Bridgers": {
        "major_key": ["Light to moderate use, typically used as 'color chords'", "Common: minor iv (e.g., Fm in C Major)"],
        "minor_key": []
    },
    "Angus & Julia Stone": { "major_key": ["Occasional use, mainly for color"], "minor_key": [] },
    "Low Roar": { "major_key": ["Occasional use, mainly for color"], "minor_key": [] },
    "Novo Amor": { "major_key": ["Occasional use, mainly for color"], "minor_key": [] },
    "SYML": { "major_key": ["Occasional use, mainly for color"], "minor_key": [] },
    "Iron & Wine": { "major_key": ["Occasional use, mainly for color"], "minor_key": [] },
    "Bon Iver": {
        "major_key": ["Heavy use of modal interchange", "Frequently borrows from parallel minor/major", "Known for chromatic harmony and unconventional chord progressions"],
        "minor_key": ["Heavy use of modal interchange", "Frequently borrows from parallel minor/major", "Known for chromatic harmony and unconventional chord progressions"]
    },
    "Leif Vollebekk": { "major_key": ["Minimal use, prefers diatonic harmony"], "minor_key": ["Minimal use, prefers diatonic harmony"] },
    "Lana Del Rey": {
        "major_key": ["Moderate to heavy use", "Often borrows from minor mode (e.g., minor iv, bVII)"],
        "minor_key": ["Moderate to heavy use", "Often borrows from major mode (e.g., Major IV)"]
    },
    "Alexandra Savior": {
        "major_key": ["Moderate use, similar to Lana Del Rey's style"],
        "minor_key": ["Moderate use, similar to Lana Del Rey's style"]
    },
    "London Grammar": { "major_key": ["Some use for atmospheric effects"], "minor_key": ["Some use for atmospheric effects"] },
    "Billie Eilish": {
        "major_key": ["Moderate use for dark, moody effects", "Often employs chromatic harmony and modal interchange"],
        "minor_key": ["Moderate use for dark, moody effects", "Often employs chromatic harmony and modal interchange"]
    },
    "EMPTY": {"major_key": [], "minor_key": []}
}

# Global variable to track adaptations visibility
show_adaptations = False

def scale_generator(root_note_name, scale_type):
    """Generates notes for a given scale type starting from a root note."""
    pattern = scale_patterns.get(scale_type)
    if not pattern:
        return []

    root_index = note_to_index_map[root_note_name]
    scale_notes = [root_note_name]
    current_index = root_index

    for interval in pattern:
        current_index = (current_index + interval) % len(notes_list)
        scale_notes.append(notes_list[current_index])

    if scale_type in chord_types_map and len(scale_notes) > 7:
        scale_notes = scale_notes[:-1]
    return scale_notes

def chords_in_scale(scale_notes, scale_type):
    """Determines the basic triad/seventh chords within a given scale."""
    chord_types = chord_types_map.get(scale_type)
    if not chord_types or len(scale_notes) < len(chord_types):
        return ["Basic chords not defined for this scale type or scale too short."]

    chords = []
    for i in range(len(chord_types)):
        note = scale_notes[i % len(scale_notes)]
        chords.append((note, chord_types[i]))
    return chords

def find_possible_scales(song_notes, allowed_scales=None):
    """Finds scales that contain all the given song notes, optionally filtered by artist style."""
    song_notes_set = set([n.upper() for n in song_notes])
    results = []
    for root in notes_list:
        for scale_type in scale_patterns:
            if allowed_scales and scale_type not in allowed_scales:
                continue
            scale_notes = scale_generator(root, scale_type)
            if song_notes_set.issubset(set([n.upper() for n in scale_notes])):
                results.append((root, scale_type, scale_notes))
    return results

def toggle_adaptations():
    """Toggle the visibility of the adaptations box."""
    global show_adaptations
    show_adaptations = not show_adaptations
    
    if show_adaptations:
        artist_adaptations_box.pack(pady=5, fill=tk.BOTH, expand=True)
        adaptations_btn.config(text="Hide Artist Adaptations")
        # Refresh results to populate the adaptations box
        if style_combo.get() != "EMPTY":
            show_results()
    else:
        artist_adaptations_box.pack_forget()
        adaptations_btn.config(text="Show Artist Adaptations")

def show_results(event=None):
    """Displays generated scales, chords, and artist-specific adaptations."""
    notes = [n.upper() for n in notes_entry.get().strip().split()]
    style = style_combo.get()

    # Always clear and update scale and chord boxes
    for box in [scale_box, chord_box]:
        box.config(state='normal')
        box.delete(1.0, tk.END)

    # Only clear adaptations box if it's visible
    if show_adaptations:
        artist_adaptations_box.config(state='normal')
        artist_adaptations_box.delete(1.0, tk.END)

    if style == "EMPTY":
        scale_box.insert(tk.END, "Choose an artist to see results.", "scale_title")
        chord_box.insert(tk.END, "")
        if show_adaptations:
            artist_adaptations_box.insert(tk.END, "Select an artist to view their typical chord extensions and borrowed chord usage.", "adapt_notes")
    else:
        allowed_scales = style_scales.get(style)
        results = find_possible_scales(notes, allowed_scales)

        if results:
            for i, (root, scale_type, scale_notes) in enumerate(results):
                scale_box.insert(tk.END, f"{root} {scale_type} scale: ", "scale_title")
                scale_box.insert(tk.END, f"{' '.join(scale_notes)}\n", "scale_notes")
                
                # Get chords as a list of (root, quality) tuples
                chords = chords_in_scale(scale_notes, scale_type)
                
                # Display Chords
                chord_box.insert(tk.END, f"{root} {scale_type} chords:\n", "chord_title")
                for chord_root, chord_quality in chords:
                    chord_box.insert(tk.END, f"  {chord_root} {chord_quality}\n", "chord_notes")
                
                # Only show adaptations if the box is visible
                if show_adaptations:
                    artist_adaptations_box.insert(tk.END, f"--- Adaptations for {root} {scale_type} ---\n\n", "adapt_title")
                    
                    # 1. Display Chord Extensions
                    artist_adaptations_box.insert(tk.END, "Extension Ideas:\n", "adapt_title")
                    artist_extensions = artist_extensions_data.get(style, [])
                    
                    if artist_extensions:
                        for chord_root, chord_quality in chords:
                            # Find compatible extensions for the current chord's quality
                            compatible_suffixes = extension_compatibility.get(chord_quality, [])
                            
                            # Find which of the artist's extensions are compatible
                            valid_extensions = [ext for ext in artist_extensions if ext in compatible_suffixes]
                            
                            if valid_extensions:
                                # Format the output string, e.g., C -> Cmaj7, Cadd9
                                extension_str = ", ".join([f"{chord_root}{ext}" for ext in valid_extensions])
                                artist_adaptations_box.insert(tk.END, f"- {chord_root} {chord_quality}: ", "adapt_notes")
                                artist_adaptations_box.insert(tk.END, f"{extension_str}\n", "adapt_notes")
                    else:
                        artist_adaptations_box.insert(tk.END, "No specific extensions noted for this artist.\n", "adapt_notes")

                    artist_adaptations_box.insert(tk.END, "\n")
                    
                    # 2. Display Borrowed Chords Usage
                    borrowed_chords_info = artist_borrowed_chords_data.get(style, {"major_key": [], "minor_key": []})
                    is_major_like = "major" in scale_type or scale_type in ["ionian", "lydian", "mixolydian"]
                    is_minor_like = "minor" in scale_type or scale_type in ["aeolian", "dorian", "phrygian", "locrian"]

                    if is_major_like and borrowed_chords_info.get("major_key"):
                        artist_adaptations_box.insert(tk.END, "Borrowed Chords (Major Context):\n", "adapt_title")
                        for desc in borrowed_chords_info["major_key"]:
                            artist_adaptations_box.insert(tk.END, f"- {desc}\n", "adapt_notes")
                    elif is_minor_like and borrowed_chords_info.get("minor_key"):
                        artist_adaptations_box.insert(tk.END, "Borrowed Chords (Minor Context):\n", "adapt_title")
                        for desc in borrowed_chords_info["minor_key"]:
                            artist_adaptations_box.insert(tk.END, f"- {desc}\n", "adapt_notes")

                    if i < len(results) - 1:
                        artist_adaptations_box.insert(tk.END, "\n" + "="*40 + "\n\n")

        else:
            scale_box.insert(tk.END, "No matching key/scale found for those notes within the selected artist's style.", "scale_title")
            chord_box.insert(tk.END, "Try different notes or a different artist.", "chord_notes")
            if show_adaptations:
                artist_adaptations_box.insert(tk.END, "No adaptations to display as no matching scale was found.", "adapt_notes")

    # Disable editing
    for box in [scale_box, chord_box]:
        box.config(state='disabled')
    if show_adaptations:
        artist_adaptations_box.config(state='disabled')

def clear_fields():
    """Clears all input and output fields."""
    notes_entry.delete(0, tk.END)
    style_combo.set("EMPTY")

    for box in [scale_box, chord_box]:
        box.config(state='normal')
        box.delete(1.0, tk.END)
        box.config(state='disabled')
    
    if show_adaptations:
        artist_adaptations_box.config(state='normal')
        artist_adaptations_box.delete(1.0, tk.END)
        artist_adaptations_box.config(state='disabled')

def on_enter(e):
    e.widget.config(bg=BTN_HOVER, fg=BG_COLOR)

def on_leave(e):
    e.widget.config(bg=BTN_COLOR, fg=TEXT_COLOR)

# --- Main Application Window Setup ---
root = tk.Tk()
root.title("INDIENIZER")
root.configure(bg=BG_COLOR)

logo_frame = tk.Frame(root, bg=BG_COLOR, bd=2, relief="flat")
logo_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
logo_label = tk.Label(logo_frame, text="♪", font=LOGO_FONT, bg=BG_COLOR, fg=ACCENT_GREY)
logo_label.pack(side=tk.LEFT, padx=10)
title_label = tk.Label(logo_frame, text="Indie Chord Generator", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR)
title_label.pack(side=tk.LEFT, padx=10)

main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

input_frame = tk.Frame(main_frame, bg=FRAME_COLOR, bd=2, relief="solid", highlightbackground=BORDER_COLOR, highlightthickness=1)
input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

result_frame = tk.Frame(main_frame, bg=FRAME_COLOR, bd=2, relief="solid", highlightbackground=BORDER_COLOR, highlightthickness=1)
result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

tk.Label(input_frame, text="Enter all notes used in your song (e.g. C D E F G A B):", font=FONT, bg=FRAME_COLOR, fg=TEXT_COLOR).pack(pady=5)
notes_entry = tk.Entry(input_frame, width=30, font=FONT, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", highlightbackground=BORDER_COLOR, highlightthickness=1)
notes_entry.pack(pady=5)
tk.Label(input_frame, text="Select artist or vibe:", font=FONT, bg=FRAME_COLOR, fg=TEXT_COLOR).pack(pady=5)
style_combo = ttk.Combobox(input_frame, values=list(style_scales.keys()), state="readonly", font=FONT)
style_combo.pack(pady=5)
style_combo.set("EMPTY")

find_btn = tk.Button(input_frame, text="Find Scales & Chords", font=FONT, bg=BTN_COLOR, fg=TEXT_COLOR, activebackground=BTN_HOVER, command=show_results, relief="flat", bd=2, highlightbackground=BORDER_COLOR, highlightthickness=1)
find_btn.pack(pady=10, fill=tk.X)
find_btn.bind("<Enter>", on_enter)
find_btn.bind("<Leave>", on_leave)

# NEW: Toggle button for adaptations
adaptations_btn = tk.Button(input_frame, text="Show Artist Adaptations", font=FONT, bg=BTN_COLOR, fg=TEXT_COLOR, activebackground=BTN_HOVER, command=toggle_adaptations, relief="flat", bd=2, highlightbackground=BORDER_COLOR, highlightthickness=1)
adaptations_btn.pack(pady=5, fill=tk.X)
adaptations_btn.bind("<Enter>", on_enter)
adaptations_btn.bind("<Leave>", on_leave)

clear_btn = tk.Button(input_frame, text="Clear", font=FONT, bg=BTN_COLOR, fg=TEXT_COLOR, activebackground=BTN_HOVER, command=clear_fields, relief="flat", bd=2, highlightbackground=BORDER_COLOR, highlightthickness=0)
clear_btn.pack(pady=5, fill=tk.X)
clear_btn.bind("<Enter>", on_enter)
clear_btn.bind("<Leave>", on_leave)
notes_entry.bind("<Return>", show_results)

scale_box = scrolledtext.ScrolledText(result_frame, width=40, height=8, font=FONT, bg=FRAME_COLOR, fg=ACCENT_BLUE, state='disabled', wrap=tk.WORD, relief="flat", highlightbackground=BORDER_COLOR, highlightthickness=0)
scale_box.pack(pady=5, fill=tk.BOTH, expand=True)
scale_box.tag_configure("scale_title", foreground=ACCENT_GREY, font=SCALE_TITLE_FONT)
scale_box.tag_configure("scale_notes", foreground=ACCENT_BLUE, font=SCALE_NOTES_FONT)

chord_box = scrolledtext.ScrolledText(result_frame, width=40, height=8, font=FONT, bg=FRAME_COLOR, fg=ACCENT_BLUE, state='disabled', wrap=tk.WORD, relief="flat", highlightbackground=BORDER_COLOR, highlightthickness=0)
chord_box.pack(pady=5, fill=tk.BOTH, expand=True)
chord_box.tag_configure("chord_title", foreground=ACCENT_GREY, font=CHORD_TITLE_FONT)
chord_box.tag_configure("chord_notes", foreground=ACCENT_BLUE, font=CHORD_NOTES_FONT)

# Adaptations box - initially hidden
artist_adaptations_box = scrolledtext.ScrolledText(result_frame, width=40, height=10, font=FONT, bg=FRAME_COLOR, fg=ACCENT_BLUE, state='disabled', wrap=tk.WORD, relief="flat", highlightbackground=BORDER_COLOR, highlightthickness=0)
artist_adaptations_box.tag_configure("adapt_title", foreground=ACCENT_GREY, font=ADAPT_TITLE_FONT)
artist_adaptations_box.tag_configure("adapt_notes", foreground=ACCENT_BLUE, font=ADAPT_NOTES_FONT)
artist_adaptations_box.tag_configure("separator", foreground=SEPARATOR_COLOR, font=ADAPT_NOTES_FONT)

clear_fields()
root.mainloop()
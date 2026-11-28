# From Zero to Legend: story plan and handoff (state on 2026-11-28)

Read this first in a new chat, together with `PRODUCTION_RULES.md` and the episode skill.

## Canon so far (what the viewers have seen)
- EP1-3: Grandad (ex-keeper, cane, white beard) gives the hero his orange gloves. The hero becomes a keeper and loses his first match 0-10. Grandad: "Keepers aren't made by saves. They're made by getting back up." Grandad collapses at the final and is taken to hospital.
- EP4: the hero stays the night at the hospital. Grandad is discharged the next day and they go to the Riverside academy trial together. The hero is late, then gets 10 minutes in a trial match and makes it. Choice: ACADEMY or HOME → ACADEMY.
- EP5: the hero is keeper No. 3 at the academy (Okafor No. 1, Dixon No. 2, rival Mason in red #9). Grandad is home on oxygen. Okafor is injured before the derby. Choice: ASK or WAIT for the shirt → ASK.
- EP6: first team vs reserves. Last kick of the shootout. Choice: LEFT or RIGHT.
- EP7 (TikTok, RIGHT): #10 baits the hero with a look, the hero dives right too early, the ball rolls into the left corner. The reserves win and Dixon gets Saturday's shirt. The coach sees the orange gloves and the red string and goes pale. Flash of 1984, Kingston v Newcastle: young Grandad (green #1, the same gloves and string) is kneed in the air by Newcastle's #9 (perm, white headband) = THE COACH. Stretcher, Grandad never played again. The coach drops his whistle and walks off. That night the hero calls Grandad: "Who is my coach?" Grandad hangs up, then texts "STAY AWAY FROM HIM." Choice: ASK COACH or STAY AWAY.
- BONUS (TikTok): the full 1984 tape, no narration. Vote: ACCIDENT or ON PURPOSE.

## Platforms (catch-up still open)
- TikTok: everything through EP7 plus the BONUS is out.
- YouTube: EP5 out (vote ASK), EP6 next (use the TikTok EP6 file, or swap only the outro to SUBSCRIBE). EP7 for YouTube depends on YouTube's EP6 vote:
  - RIGHT = the same video, with only the outro changed.
  - LEFT = render with `VOTE=LEFT` (the hero saves and gets the shirt), plus a short voice patch for lines 1-5.
- From EP8 on: ONE video for both platforms. Add up the votes from both. Neutral outro: "SEE YOU IN PART N".

## The creator's plan for the next arc
1. Riverside does NOT keep him (he is let go from the academy). But at that game a scout from Spain notices him.
2. He goes to Spain and trains very hard. Show the training (montages, counters, failures).
3. A selection camp in the spirit of the anime Blue Lock: games and elimination rounds, more or less like that.
   - The camp must be OUR OWN, not a copy: our own name, rules, characters and look. No Blue Lock names, terms or designs.
4. We need very strong characters who are revealed as the story goes.
5. EP6 had very epic shots. Every episode needs 2-3 shots like that.

## Proposal: how to link it to the canon
EP8-EP9 (end of the Riverside arc):
- Whatever the vote (ASK COACH / STAY AWAY), the coach cuts him: "Riverside doesn't need you." Viewers sense the real reason is 1984, not football. Mason smirks, Dixon is quiet.
- At the Saturday derby the hero is in the stand or warms up as the sub. Dixon is hurt in the 80th minute. The hero gets 10 minutes and makes one impossible save (an epic shot).
- In the stand sits an old man in a long coat: DON RAMIRO, a scout from Spain. He knew Grandad in 1984. He recognises the gloves.
- Cliffhanger: a card "CLUB ATLETICO DEL SOL — ACADEMY, VALENCIA" (fictional club). Choice: GO TO SPAIN or STAY WITH GRANDAD (Grandad: "Go. This time, go.").

EP10-EP13 (Spain, training):
- A new country, a language he doesn't speak, heat, 6 a.m. on the beach. Training counters ("DAY 14 · DIVES 3,000").
- He gets everything wrong, the others laugh. A video call with Grandad. Alfie writes from home.
- The camp's coach: ISABEL NAVARRO, "LA DAMA DE HIERRO", a former Spanish national keeper. Brutal methods (keeping goal in the sand against tennis-ball cannons, blindfold drills).

EP14+ (the selection camp: our own format, "LA JAULA / THE CAGE"):
- 48 boys, one stadium, one rule: every week half go home. On screen: a ranking table (No. 1-48), the hero's number at the bottom.
- Rounds: 1v1 keeper vs striker, "3 against the keeper", "last minute 0-1", "one save = one place".
- Every round gives an EPIC frame: bullet time, a frozen mid-air dive, the camera inside the net, a silhouette against the floodlights, POV gloves.

## Strong characters (revealed gradually)
- RAFA ORTEGA "EL MURO": a Spanish keeper, 15, almost 2 m tall, never smiles, ranked No. 1. Main rival.
  - Secret: plays to pay his family's debts.
- KENJI MORI: a Japanese striker with an impossible curl. Quiet, reads a keeper's knees.
  - Arc: from enemy to friend. Teaches the hero to "read the striker" (a callback to EP7's bait).
- AMARA OKOYE: the fastest winger in the camp, cheerful, the hero's first friend in Spain.
  - Secret: an injury she hides from the coaches.
- LUCA BENEDETTI: an Italian genius and showman, arrogant, films everything for his followers.
  - Arc: a villain who becomes an ally in the final.
- DON RAMIRO: the scout. Was at the 1984 game and knows the truth about the knee (accident or on purpose).
- ISABEL NAVARRO: the camp's coach. Her methods are cruel, but she sees the hero's potential.
- Return later: MASON arrives at the camp from England as a striker (rival → ally). The COACH from Riverside comes to Spain at the end of the arc for a reckoning.

## Epic shots: 2-3 per episode (EP6 level)
Frozen mid-air dive + speed lines; ball flying at the camera; camera inside the net; a slow-mo frozen moment at the decisive kick; a silhouette against the floodlights in the rain; POV gloves; a top-down shot of a keeper lying on the grass; a VHS memory; a dolly zoom on a face; a full-screen ranking reveal. NO split screens (the creator dislikes them). No speech bubbles.

## Technical state
- Sources for the current episode: `ep7/src/` (`ep7.py` = the episode, `fb84.py` = the 1984 scenes, `cast84.py`, `style.py`, `persp.py`, `sfx7.py`, `voice7.py`, `mix7.py`, `render7.py`, `bonus1984.py`).
- Keeper's view with a real 3D goal: `GoalCam` and `posts_fg` in `ep7.py`. Animated run-up, front-on strike pose `strikeF`, `watchers`.
- Voice: ElevenLabs George `JBFqnCBsd6RMkjVDRZzb`, model `eleven_v4`, one take. The sandbox cannot download from elevenlabsusercontent.com, so the creator uploads the mp3.
- QA: a reviewer agent at 0.1 s per frame; for big changes, two agents (errors + direction).

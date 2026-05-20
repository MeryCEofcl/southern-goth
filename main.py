from flask import Flask, render_template_string

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Southern Goth — Historia de la Cultura Gótica</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500&family=IM+Fell+English:ital@0;1&display=swap" rel="stylesheet">
    <style>
        /* ══════════════════════════════════════
           VARIABLES & RESET
        ══════════════════════════════════════ */
        :root {
            --ink:    #0c0d0a;
            --ash:    #d4cfc5;
            --bone:   #bfb9a8;
            --moss:   #6e7857;
            --sage:   #8f9878;
            --blood:  #8b2020;
            --amber:  #a07840;
            --mist:   rgba(210,205,192,0.05);
            --border: rgba(180,174,158,0.13);
        }

        *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
        html { scroll-behavior: smooth; }

        /* ══════════════════════════════════════
           CURSOR PERSONALIZADO — Cruz caligráfica
        ══════════════════════════════════════ */
        body {
            background-color: var(--ink);
            background-image:
                radial-gradient(ellipse 80% 60% at 50% 0%,  rgba(72,78,58,0.22) 0%, transparent 70%),
                radial-gradient(ellipse 60% 40% at 20% 80%, rgba(80,55,40,0.12) 0%, transparent 60%);
            color: var(--ash);
            font-family: 'Cormorant Garamond', serif;
            overflow-x: hidden;
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 28 28'%3E%3Cline x1='14' y1='2' x2='14' y2='26' stroke='%238f9878' stroke-width='1.2' opacity='0.85'/%3E%3Cline x1='4' y1='10' x2='24' y2='10' stroke='%238f9878' stroke-width='1.2' opacity='0.85'/%3E%3Ccircle cx='14' cy='14' r='2' fill='%236e7857' opacity='0.6'/%3E%3C/svg%3E") 14 14, crosshair;
        }

        /* ══════════════════════════════════════
           NOISE OVERLAY
        ══════════════════════════════════════ */
        body::before {
            content:'';
            position:fixed; inset:0;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='512' height='512' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
            pointer-events:none; z-index:9998; opacity:0.45;
        }

        ::-webkit-scrollbar { width:3px; }
        ::-webkit-scrollbar-track { background:var(--ink); }
        ::-webkit-scrollbar-thumb { background:var(--moss); }

        /* ══════════════════════════════════════
           LOADING SCREEN
        ══════════════════════════════════════ */
        #loader {
            position: fixed;
            inset: 0;
            background: #080908;
            z-index: 99999;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 2rem;
            transition: opacity 0.8s ease, visibility 0.8s ease;
        }

        #loader.hidden { opacity:0; visibility:hidden; }

        .loader-cross {
            font-size: 2.5rem;
            color: var(--moss);
            animation: loaderPulse 1.8s ease-in-out infinite;
        }

        @keyframes loaderPulse {
            0%,100% { opacity:0.2; transform: scale(0.95); }
            50%      { opacity:1;   transform: scale(1.05); }
        }

        .loader-title {
            font-family: 'Cinzel', serif;
            font-size: clamp(1.2rem, 4vw, 2rem);
            letter-spacing: 14px;
            color: var(--ash);
            opacity: 0;
            animation: loaderFade 1.8s ease 0.4s forwards;
        }

        @keyframes loaderFade {
            from { opacity:0; transform:translateY(10px); }
            to   { opacity:1; transform:translateY(0); }
        }

        .loader-bar-wrap {
            width: 180px;
            height: 1px;
            background: rgba(110,120,87,0.2);
            position: relative;
            overflow: hidden;
        }

        .loader-bar {
            position: absolute;
            left: -100%;
            top: 0; bottom: 0;
            width: 100%;
            background: linear-gradient(to right, transparent, var(--moss), transparent);
            animation: loaderBar 1.6s ease 0.3s forwards;
        }

        @keyframes loaderBar {
            from { left:-100%; }
            to   { left:100%; }
        }

        /* ══════════════════════════════════════
           NAV
        ══════════════════════════════════════ */
        nav {
            position:fixed; top:0; left:0; right:0; z-index:100;
            display:flex; justify-content:space-between; align-items:center;
            padding:1.2rem 4rem;
            background:linear-gradient(to bottom, rgba(12,13,10,0.96), transparent);
            backdrop-filter:blur(4px);
        }

        .nav-logo {
            font-family:'Cinzel',serif; font-size:0.85rem;
            letter-spacing:6px; color:var(--sage); text-decoration:none;
        }

        .nav-links { display:flex; gap:2.2rem; list-style:none; }

        .nav-links a {
            font-family:'Cinzel',serif; font-size:0.65rem; letter-spacing:3px;
            color:var(--bone); text-decoration:none; opacity:0.5;
            transition:opacity 0.3s, color 0.3s; text-transform:uppercase;
        }

        .nav-links a:hover { opacity:1; color:var(--ash); }

        /* ══════════════════════════════════════
           PROGRESS DOTS (navegación lateral)
        ══════════════════════════════════════ */
        #progress-nav {
            position: fixed;
            right: 1.6rem;
            top: 50%;
            transform: translateY(-50%);
            z-index: 200;
            display: flex;
            flex-direction: column;
            gap: 0.9rem;
            align-items: center;
        }

        .prog-dot {
            width: 6px; height: 6px;
            border-radius: 50%;
            background: rgba(143,152,120,0.3);
            border: 1px solid rgba(143,152,120,0.4);
            cursor: pointer;
            transition: background 0.4s, transform 0.4s, height 0.4s;
            position: relative;
        }

        .prog-dot.active {
            background: var(--sage);
            height: 18px;
            border-radius: 3px;
        }

        .prog-dot:hover { background: var(--moss); transform: scale(1.3); }

        .prog-dot .dot-label {
            position: absolute;
            right: 16px;
            top: 50%;
            transform: translateY(-50%);
            font-family: 'Cinzel', serif;
            font-size: 0.55rem;
            letter-spacing: 2px;
            color: var(--sage);
            white-space: nowrap;
            opacity: 0;
            transition: opacity 0.3s;
            pointer-events: none;
        }

        .prog-dot:hover .dot-label { opacity: 1; }

        @media(max-width:768px) { #progress-nav { display:none; } }

        /* ══════════════════════════════════════
           HERO
        ══════════════════════════════════════ */
        header {
            height:100vh;
            display:flex; flex-direction:column;
            justify-content:center; align-items:center; text-align:center;
            padding:2rem; position:relative; overflow:hidden;
        }

        .hero-bg {
            position:absolute; inset:0;
            background:
                linear-gradient(rgba(12,13,10,0.72) 0%, rgba(12,13,10,0.5) 50%, rgba(12,13,10,0.92) 100%),
                url('https://news.emory.edu/stories/2024/10/er_cinematheque_season_02-10-2024/thumbs/story_main.jpg') center/cover no-repeat;
            animation: slowZoom 30s ease-in-out infinite alternate;
        }

        @keyframes slowZoom {
            from { transform:scale(1); }
            to   { transform:scale(1.07); }
        }

        /* Forma diagonal inferior del hero */
        header::after {
            content:'';
            position:absolute;
            bottom:-1px; left:0; right:0;
            height:80px;
            background:var(--ink);
            clip-path: polygon(0 100%, 100% 0, 100% 100%);
        }

        .hero-frame {
            position:absolute; inset:3rem;
            border:1px solid rgba(143,152,120,0.15);
            pointer-events:none;
        }

        .hero-frame::before, .hero-frame::after {
            content:''; position:absolute;
            width:20px; height:20px;
            border-color:var(--sage); border-style:solid; opacity:0.45;
        }

        .hero-frame::before { top:-1px; left:-1px; border-width:1px 0 0 1px; }
        .hero-frame::after  { bottom:-1px; right:-1px; border-width:0 1px 1px 0; }

        .hero-content {
            position:relative; z-index:2;
            animation:fadeUp 1.8s ease forwards;
        }

        @keyframes fadeUp {
            from { opacity:0; transform:translateY(30px); }
            to   { opacity:1; transform:translateY(0); }
        }

        .hero-ornament {
            font-size:1.8rem; color:var(--moss);
            letter-spacing:16px; margin-bottom:1.8rem; opacity:0.65;
            /* efecto vela en el ornamento */
            animation: candleFlicker 6s ease-in-out infinite;
        }

        h1 {
            font-family:'Cinzel',serif;
            font-size:clamp(2.8rem, 8vw, 7rem);
            letter-spacing:12px; color:var(--ash);
            text-shadow:0 0 60px rgba(0,0,0,0.9);
            line-height:1; margin-bottom:0.3rem;
        }

        .hero-sub-title {
            font-family:'Cinzel',serif;
            font-size:clamp(0.65rem, 1.5vw, 0.9rem);
            letter-spacing:8px; color:var(--sage);
            margin-bottom:2rem; opacity:0.75;
        }

        .hero-desc {
            font-family:'IM Fell English',serif; font-style:italic;
            font-size:clamp(1rem, 2vw, 1.45rem);
            max-width:660px; color:var(--bone); line-height:1.85; opacity:0.85;
        }

        .scroll-hint {
            position:absolute; bottom:5.5rem; left:50%; transform:translateX(-50%);
            display:flex; flex-direction:column; align-items:center; gap:0.5rem;
            opacity:0.35; animation:float 3s ease-in-out infinite; z-index:2;
        }

        .scroll-hint span {
            font-family:'Cinzel',serif; font-size:0.55rem; letter-spacing:4px; color:var(--sage);
        }

        .scroll-line { width:1px; height:45px; background:linear-gradient(to bottom, var(--sage), transparent); }

        @keyframes float {
            0%,100% { transform:translateX(-50%) translateY(0); }
            50%      { transform:translateX(-50%) translateY(8px); }
        }

        /* ══════════════════════════════════════
           EFECTO VELA / PARPADEO
        ══════════════════════════════════════ */
        @keyframes candleFlicker {
            0%,100% { opacity:0.65; text-shadow: 0 0 8px rgba(110,120,87,0.3); }
            15%     { opacity:0.55; text-shadow: 0 0 4px rgba(110,120,87,0.1); }
            30%     { opacity:0.7;  text-shadow: 0 0 12px rgba(110,120,87,0.5); }
            50%     { opacity:0.6;  text-shadow: 0 0 6px rgba(110,120,87,0.2); }
            70%     { opacity:0.68; text-shadow: 0 0 10px rgba(110,120,87,0.4); }
            85%     { opacity:0.5;  text-shadow: 0 0 3px rgba(110,120,87,0.1); }
        }

        .candle { animation: candleFlicker 5s ease-in-out infinite; }
        .candle-slow { animation: candleFlicker 8s ease-in-out infinite 1s; }

        /* ══════════════════════════════════════
           SECTION BASE
        ══════════════════════════════════════ */
        section {
            max-width:1100px; margin:0 auto;
            padding:8rem 3rem;
            position:relative;
            opacity:0; transform:translateY(40px);
            transition:opacity 0.9s ease, transform 0.9s ease;
        }

        section.visible { opacity:1; transform:translateY(0); }

        /* Separador diagonal entre secciones */
        .section-divider {
            width:100%; height:60px; overflow:hidden; line-height:0;
        }

        .section-divider svg { width:100%; height:60px; }

        .section-eyebrow {
            font-family:'Cinzel',serif; font-size:0.62rem; letter-spacing:5px;
            color:var(--moss); text-transform:uppercase; margin-bottom:0.9rem;
            display:flex; align-items:center; gap:1rem;
        }

        .section-eyebrow::after {
            content:''; flex:1; max-width:60px; height:1px;
            background:var(--moss); opacity:0.4;
        }

        .section-title {
            font-family:'Cinzel',serif;
            font-size:clamp(1.8rem, 4vw, 3rem);
            color:var(--ash); margin-bottom:3rem; line-height:1.2;
        }

        p {
            font-size:1.28rem; line-height:2;
            margin-bottom:1.8rem; color:#cac4b5; font-weight:300;
        }

        /* ══════════════════════════════════════
           QUOTE — CON ACENTO SANGRE/ÁMBAR
        ══════════════════════════════════════ */
        .quote {
            margin:3rem 0; padding:2rem 2.5rem;
            border-left:2px solid var(--blood);
            background:rgba(139,32,32,0.04);
            font-family:'IM Fell English',serif; font-style:italic;
            font-size:1.35rem; color:var(--bone); line-height:1.75;
            position:relative;
        }

        .quote::before {
            content:'"'; font-family:'Cinzel',serif; font-size:5rem;
            color:var(--blood); opacity:0.18;
            position:absolute; top:-0.8rem; left:1rem; line-height:1;
        }

        .quote-author {
            display:block; font-style:normal; font-size:0.8rem;
            letter-spacing:3px; color:var(--amber); margin-top:0.9rem;
            font-family:'Cinzel',serif;
        }

        /* ══════════════════════════════════════
           CITAS ROTATIVAS
        ══════════════════════════════════════ */
        #rotating-quotes {
            max-width:800px; margin:0 auto;
            text-align:center; padding:6rem 2rem;
            border-top:1px solid var(--border);
            border-bottom:1px solid var(--border);
            position:relative;
            opacity:0; transform:translateY(40px);
            transition:opacity 0.9s ease, transform 0.9s ease;
        }

        #rotating-quotes.visible { opacity:1; transform:translateY(0); }

        .rq-ornament {
            font-size:1.5rem; color:var(--blood); opacity:0.4;
            margin-bottom:2rem;
            animation: candleFlicker 7s ease-in-out infinite;
        }

        .rq-text {
            font-family:'IM Fell English',serif; font-style:italic;
            font-size:clamp(1.3rem, 2.5vw, 1.8rem);
            color:var(--bone); line-height:1.7;
            min-height:120px;
            transition:opacity 0.7s ease;
        }

        .rq-text.fade { opacity:0; }

        .rq-author {
            margin-top:1.5rem;
            font-family:'Cinzel',serif; font-size:0.7rem;
            letter-spacing:4px; color:var(--amber); opacity:0.75;
            transition:opacity 0.7s ease;
        }

        .rq-author.fade { opacity:0; }

        .rq-dots {
            display:flex; justify-content:center; gap:0.6rem; margin-top:2rem;
        }

        .rq-dot {
            width:5px; height:5px; border-radius:50%;
            background:rgba(143,152,120,0.3);
            transition:background 0.4s;
        }

        .rq-dot.active { background:var(--moss); }

        /* ══════════════════════════════════════
           CARDS
        ══════════════════════════════════════ */
        .cards {
            display:grid; grid-template-columns:repeat(auto-fit, minmax(255px,1fr));
            gap:1.5rem; margin-top:3rem;
        }

        .card {
            background:rgba(16,18,14,0.85);
            border:1px solid var(--border);
            padding:2rem; border-radius:1px;
            transition:transform 0.4s, border-color 0.4s, box-shadow 0.4s;
            position:relative; overflow:hidden;
        }

        .card::after {
            content:''; position:absolute;
            bottom:0; left:0; right:0; height:2px;
            background:linear-gradient(to right, var(--blood), transparent);
            transform:scaleX(0); transform-origin:left;
            transition:transform 0.4s ease;
        }

        .card:hover { transform:translateY(-6px); border-color:rgba(139,32,32,0.3); box-shadow:0 12px 40px rgba(0,0,0,0.4); }
        .card:hover::after { transform:scaleX(1); }

        .card-icon { font-size:1.7rem; margin-bottom:1rem; display:block; opacity:0.55; }

        .card h3 {
            font-family:'Cinzel',serif; color:var(--ash);
            margin-bottom:0.7rem; font-size:1.05rem; letter-spacing:1px;
        }

        .card p { font-size:1.05rem; color:#b0aa9c; margin:0; }

        /* ══════════════════════════════════════
           GALERÍA DE IMÁGENES
        ══════════════════════════════════════ */
        #gallery {
            max-width:1200px; margin:0 auto; padding:8rem 3rem;
            opacity:0; transform:translateY(40px);
            transition:opacity 0.9s ease, transform 0.9s ease;
        }

        #gallery.visible { opacity:1; transform:translateY(0); }

        .gallery-grid {
            display:grid;
            grid-template-columns: 2fr 1fr 1fr;
            grid-template-rows: 260px 260px;
            gap:6px; margin-top:3rem;
        }

        @media(max-width:768px) {
            .gallery-grid {
                grid-template-columns:1fr 1fr;
                grid-template-rows:repeat(3, 200px);
            }
        }

        .gallery-item {
            overflow:hidden; position:relative; cursor:pointer;
        }

        .gallery-item:first-child {
            grid-row: span 2;
        }

        .gallery-item img {
            width:100%; height:100%; object-fit:cover;
            filter:grayscale(40%) brightness(0.75) contrast(1.1);
            transition:transform 0.7s ease, filter 0.5s ease;
        }

        .gallery-item:hover img {
            transform:scale(1.06);
            filter:grayscale(10%) brightness(0.85) contrast(1.05);
        }

        .gallery-caption {
            position:absolute; bottom:0; left:0; right:0;
            padding:1rem 1.2rem;
            background:linear-gradient(to top, rgba(12,13,10,0.85), transparent);
            font-family:'Cinzel',serif; font-size:0.65rem; letter-spacing:2px;
            color:var(--sage); opacity:0;
            transition:opacity 0.4s;
        }

        .gallery-item:hover .gallery-caption { opacity:1; }

        /* Lightbox */
        #lightbox {
            position:fixed; inset:0; z-index:9990;
            background:rgba(12,13,10,0.96);
            display:flex; align-items:center; justify-content:center;
            opacity:0; visibility:hidden;
            transition:opacity 0.4s, visibility 0.4s;
        }

        #lightbox.open { opacity:1; visibility:visible; }

        #lightbox img {
            max-width:88vw; max-height:85vh;
            object-fit:contain;
            filter:grayscale(20%) brightness(0.9);
            border:1px solid var(--border);
        }

        #lightbox-close {
            position:absolute; top:2rem; right:2.5rem;
            font-family:'Cinzel',serif; font-size:0.75rem; letter-spacing:3px;
            color:var(--sage); cursor:pointer; opacity:0.6;
            transition:opacity 0.3s;
            background:none; border:none;
        }

        #lightbox-close:hover { opacity:1; }

        /* ══════════════════════════════════════
           TIMELINE
        ══════════════════════════════════════ */
        .timeline { margin-top:4rem; position:relative; }

        .timeline::before {
            content:''; position:absolute;
            left:0; top:0; bottom:0; width:1px;
            background:linear-gradient(to bottom, transparent, var(--moss), transparent);
            opacity:0.35;
        }

        .timeline-item { padding-left:3rem; padding-bottom:3.5rem; position:relative; }
        .timeline-item:last-child { padding-bottom:0; }

        .timeline-dot {
            position:absolute; left:-5px; top:8px;
            width:11px; height:11px;
            background:var(--blood); border-radius:50%;
            box-shadow:0 0 12px rgba(139,32,32,0.5);
        }

        .year {
            font-family:'Cinzel',serif; font-size:0.82rem;
            letter-spacing:3px; color:var(--amber); margin-bottom:0.5rem;
        }

        .timeline-item p { font-size:1.15rem; margin:0; }

        /* ══════════════════════════════════════
           BANDS GRID
        ══════════════════════════════════════ */
        .bands-grid {
            display:grid; grid-template-columns:repeat(auto-fit, minmax(200px,1fr));
            gap:1px; margin-top:3rem; background:var(--border);
        }

        .band-cell {
            background:var(--ink); padding:2rem 1.5rem;
            transition:background 0.3s; position:relative; overflow:hidden;
        }

        .band-cell::before {
            content:''; position:absolute;
            top:0; left:0; width:2px; height:0;
            background:var(--blood);
            transition:height 0.4s ease;
        }

        .band-cell:hover { background:rgba(20,22,17,0.9); }
        .band-cell:hover::before { height:100%; }

        .band-name { font-family:'Cinzel',serif; font-size:0.95rem; color:var(--ash); margin-bottom:0.3rem; }
        .band-genre { font-size:0.72rem; letter-spacing:2px; color:var(--amber); font-family:'Cinzel',serif; text-transform:uppercase; margin-bottom:0.7rem; }
        .band-cell p { font-size:1rem; color:#aba598; margin:0; line-height:1.6; }

        /* ══════════════════════════════════════
           FILMS GRID
        ══════════════════════════════════════ */
        .films-grid {
            display:grid; grid-template-columns:repeat(auto-fit, minmax(240px,1fr));
            gap:1.5rem; margin-top:3rem;
        }

        .film-card {
            border:1px solid var(--border);
            padding:1.8rem;
            position:relative; overflow:hidden;
            transition:border-color 0.4s, background 0.4s;
        }

        .film-card:hover { border-color:rgba(139,32,32,0.35); background:rgba(139,32,32,0.04); }

        .film-year {
            font-family:'Cinzel',serif; font-size:0.65rem; letter-spacing:3px;
            color:var(--blood); margin-bottom:0.7rem; opacity:0.8;
        }

        .film-title {
            font-family:'Cinzel',serif; font-size:1.05rem; color:var(--ash);
            margin-bottom:0.7rem; line-height:1.3;
        }

        .film-card p { font-size:1rem; color:#b0aa9c; margin:0; line-height:1.6; }

        /* ══════════════════════════════════════
           SYMBOLS ROW
        ══════════════════════════════════════ */
        .symbols-row {
            display:flex; flex-wrap:wrap; gap:1rem; margin-top:2.5rem;
        }

        .symbol-tag {
            display:flex; align-items:center; gap:0.5rem;
            padding:0.5rem 1rem;
            border:1px solid var(--border);
            font-family:'Cinzel',serif; font-size:0.7rem; letter-spacing:2px;
            color:var(--bone); opacity:0.65;
            transition:opacity 0.3s, border-color 0.3s, color 0.3s;
        }

        .symbol-tag:hover { opacity:1; border-color:var(--blood); color:var(--ash); }

        /* ══════════════════════════════════════
           TWO-COL
        ══════════════════════════════════════ */
        .two-col { display:grid; grid-template-columns:1fr 1fr; gap:5rem; align-items:start; }

        @media(max-width:900px) {
            .two-col { grid-template-columns:1fr; gap:2rem; }
            nav { padding:1rem 1.5rem; }
            .nav-links { display:none; }
            section { padding:5rem 1.5rem; }
            .gallery-grid { grid-template-columns:1fr; grid-template-rows:repeat(5,200px); }
            .gallery-item:first-child { grid-row:span 1; }
        }

        /* ══════════════════════════════════════
           PHILOSOPHY
        ══════════════════════════════════════ */
        .philosophy-grid {
            display:grid; grid-template-columns:repeat(3,1fr);
            gap:0; margin-top:3rem;
            border:1px solid var(--border);
        }

        @media(max-width:768px) { .philosophy-grid { grid-template-columns:1fr; } }

        .phil-item {
            padding:2.5rem 2rem; border-right:1px solid var(--border); position:relative;
        }

        .phil-item:last-child { border-right:none; }

        .phil-number {
            font-family:'Cinzel',serif; font-size:4rem; color:var(--blood);
            opacity:0.1; position:absolute; top:1rem; right:1.5rem; line-height:1;
        }

        .phil-item h3 {
            font-family:'Cinzel',serif; font-size:0.95rem; letter-spacing:2px;
            color:var(--sage); margin-bottom:1rem;
        }

        .phil-item p { font-size:1.05rem; line-height:1.75; color:#b0aa9b; margin:0; }

        /* ══════════════════════════════════════
           FIGURES
        ══════════════════════════════════════ */
        .figures-list { margin-top:3rem; }

        .figure-row {
            display:grid; grid-template-columns:180px 1fr;
            gap:2rem; padding:2rem 0;
            border-bottom:1px solid var(--border); align-items:start;
        }

        .figure-row:last-child { border-bottom:none; }

        .figure-name { font-family:'Cinzel',serif; font-size:0.95rem; color:var(--ash); letter-spacing:1px; }
        .figure-date { font-size:0.72rem; letter-spacing:2px; color:var(--amber); font-family:'Cinzel',serif; margin-top:0.3rem; }
        .figure-row p { font-size:1.1rem; color:#b5b0a2; margin:0; line-height:1.75; }

        /* ══════════════════════════════════════
           SOUTHERN GOTHIC
        ══════════════════════════════════════ */
        .sg-features {
            display:grid; grid-template-columns:repeat(2,1fr);
            gap:2px; margin-top:3rem; background:var(--border);
        }

        @media(max-width:768px) { .sg-features { grid-template-columns:1fr; } }

        .sg-feat { background:var(--ink); padding:2.5rem 2rem; }

        .sg-feat h3 {
            font-family:'Cinzel',serif; font-size:0.85rem; letter-spacing:3px;
            color:var(--sage); margin-bottom:1rem; text-transform:uppercase;
        }

        .sg-feat p { font-size:1.1rem; color:#aba598; margin:0; line-height:1.7; }

        /* ══════════════════════════════════════
           FOOTER
        ══════════════════════════════════════ */
        footer {
            padding:5rem 3rem; text-align:center; position:relative;
            clip-path: polygon(0 20px, 100% 0, 100% 100%, 0 100%);
            background:rgba(8,9,7,0.6);
            margin-top:-20px;
        }

        footer::before {
            content:''; display:block; width:1px; height:60px;
            background:linear-gradient(to bottom, var(--blood), transparent);
            margin:0 auto 2rem; opacity:0.35;
        }

        .footer-logo {
            font-family:'Cinzel',serif; font-size:0.65rem; letter-spacing:8px;
            color:var(--moss); opacity:0.55; margin-bottom:0.8rem;
            animation: candleFlicker 9s ease-in-out infinite;
        }

        .footer-text { font-size:0.8rem; color:#5a5850; letter-spacing:2px; }

        /* ══════════════════════════════════════
           DIVIDER ORNAMENT
        ══════════════════════════════════════ */
        .divider {
            display:flex; align-items:center; gap:1.5rem; margin:3rem 0; opacity:0.25;
        }

        .divider::before, .divider::after {
            content:''; flex:1; height:1px; background:var(--sage);
        }

        .divider span { font-family:'Cinzel',serif; font-size:0.9rem; color:var(--sage); }

        .highlight { color:var(--amber); font-style:italic; }

        /* ══════════════════════════════════════
           MUSIC PLAYER
        ══════════════════════════════════════ */
        #music-player {
            position:fixed; bottom:2rem; right:2rem; z-index:9000;
            display:flex; align-items:center; gap:1rem;
            background:rgba(12,13,10,0.9);
            border:1px solid rgba(110,120,87,0.28);
            backdrop-filter:blur(12px);
            padding:0.8rem 1.2rem;
            box-shadow:0 4px 30px rgba(0,0,0,0.5);
            animation:slideInPlayer 1s ease 3s both;
            transition:border-color 0.3s;
        }

        #music-player:hover { border-color:rgba(139,32,32,0.4); }

        @keyframes slideInPlayer {
            from { opacity:0; transform:translateY(20px); }
            to   { opacity:1; transform:translateY(0); }
        }

        #music-icon {
            font-size:1rem; color:var(--moss);
            animation:candleFlicker 3s ease-in-out infinite;
        }

        #music-title { font-family:'Cinzel',serif; font-size:0.65rem; letter-spacing:2px; color:var(--ash); white-space:nowrap; }
        #music-artist { font-family:'Cormorant Garamond',serif; font-size:0.75rem; color:var(--amber); margin-top:0.1rem; }

        #music-toggle {
            background:none;
            border:1px solid rgba(139,32,32,0.35);
            color:var(--sage); font-size:0.85rem;
            width:30px; height:30px;
            display:flex; align-items:center; justify-content:center;
            cursor:pointer; transition:background 0.3s, border-color 0.3s;
        }

        #music-toggle:hover { background:rgba(139,32,32,0.12); border-color:var(--blood); }

        #music-player.paused #music-icon { animation:none; opacity:0.35; }
    </style>
</head>
<body>

<!-- ══ LOADER ══ -->
<div id="loader">
    <div class="loader-cross">✟</div>
    <div class="loader-title">SOUTHERN GOTH</div>
    <div class="loader-bar-wrap"><div class="loader-bar"></div></div>
</div>

<!-- ══ PROGRESS DOTS ══ -->
<div id="progress-nav">
    <div class="prog-dot active" data-target="hero">
        <span class="dot-label">Inicio</span>
    </div>
    <div class="prog-dot" data-target="origen">
        <span class="dot-label">Origen</span>
    </div>
    <div class="prog-dot" data-target="cronologia">
        <span class="dot-label">Cronología</span>
    </div>
    <div class="prog-dot" data-target="musica">
        <span class="dot-label">Música</span>
    </div>
    <div class="prog-dot" data-target="subculturas">
        <span class="dot-label">Subculturas</span>
    </div>
    <div class="prog-dot" data-target="figuras">
        <span class="dot-label">Figuras</span>
    </div>
    <div class="prog-dot" data-target="filosofia">
        <span class="dot-label">Filosofía</span>
    </div>
    <div class="prog-dot" data-target="cine">
        <span class="dot-label">Cine</span>
    </div>
    <div class="prog-dot" data-target="galeria">
        <span class="dot-label">Galería</span>
    </div>
    <div class="prog-dot" data-target="southern">
        <span class="dot-label">Southern</span>
    </div>
</div>

<!-- ══ NAV ══ -->
<nav>
    <a href="#" class="nav-logo">✟ SOUTHERN GOTH</a>
    <ul class="nav-links">
        <li><a href="#origen">Origen</a></li>
        <li><a href="#cronologia">Cronología</a></li>
        <li><a href="#musica">Música</a></li>
        <li><a href="#subculturas">Subculturas</a></li>
        <li><a href="#figuras">Figuras</a></li>
        <li><a href="#filosofia">Filosofía</a></li>
        <li><a href="#cine">Cine</a></li>
        <li><a href="#southern">Southern</a></li>
    </ul>
</nav>

<!-- ══ HERO ══ -->
<header id="hero">
    <div class="hero-bg"></div>
    <div class="hero-frame"></div>
    <div class="hero-content">
        <div class="hero-ornament">✦ ✟ ✦</div>
        <h1>SOUTHERN GOTH</h1>
        <p class="hero-sub-title">Historia de la Cultura Gótica</p>
        <p class="hero-desc">
            Un recorrido por la historia de la cultura gótica, sus raíces musicales,
            artísticas y espirituales, envuelto en la decadencia romántica del southern gothic.
        </p>
    </div>
    <div class="scroll-hint">
        <span>Explorar</span>
        <div class="scroll-line"></div>
    </div>
</header>

<!-- ══ CITAS ROTATIVAS ══ -->
<div id="rotating-quotes">
    <div class="rq-ornament">✟</div>
    <div class="rq-text"></div>
    <div class="rq-author"></div>
    <div class="rq-dots"></div>
</div>

<!-- ══ ORIGEN ══ -->
<section id="origen">
    <p class="section-eyebrow">I — Comienzos</p>
    <h2 class="section-title">¿Cómo empezó todo?</h2>
    <div class="two-col">
        <div>
            <p>La cultura gótica moderna nació en el <span class="highlight">Reino Unido a finales de los años 70</span>, derivada directamente del post-punk. Mientras el punk expresaba rabia y anarquía, el goth comenzó a explorar emociones más profundas: la melancolía, la muerte, el romanticismo oscuro y la belleza en la decadencia.</p>
            <p>Bandas como Joy Division, Bauhaus y Siouxsie and the Banshees desarrollaron un sonido denso, oscuro y poético que se convirtió en el núcleo de la identidad gótica. El término "goth" como movimiento subcultural se consolidó hacia 1982.</p>
        </div>
        <div>
            <p>Sus raíces vienen de mucho antes. La <span class="highlight">arquitectura gótica medieval</span>, las catedrales religiosas con sus arcos apuntados y gárgolas, las novelas victorianas y la literatura de terror del siglo XVIII ayudaron a construir toda la estética que más tarde definiría el movimiento.</p>
            <div class="quote">
                "El goth no trata sobre la muerte. Trata sobre encontrar belleza en la oscuridad."
            </div>
        </div>
    </div>
    <div class="symbols-row">
        <div class="symbol-tag">✟ Cruz</div>
        <div class="symbol-tag">⚰ Memento Mori</div>
        <div class="symbol-tag">🌹 Rosa negra</div>
        <div class="symbol-tag">🦇 Murciélago</div>
        <div class="symbol-tag">🕯 Candelabro</div>
        <div class="symbol-tag">🌙 Luna</div>
        <div class="symbol-tag">💀 Calavera</div>
        <div class="symbol-tag">🐦‍⬛ Cuervo</div>
    </div>
</section>

<!-- ══ CRONOLOGÍA ══ -->
<section id="cronologia">
    <p class="section-eyebrow">II — Cronología</p>
    <h2 class="section-title">Línea del Tiempo</h2>
    <div class="timeline">
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="year">Siglo XII — XIV</div>
            <p>Nace el arte gótico medieval en Europa con enormes catedrales, vitrales polícromos, gárgolas y simbolismo religioso. La Catedral de Notre Dame es el máximo exponente de esta estética de lo sublime oscuro.</p>
        </div>
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="year">1764 — Novela Gótica</div>
            <p>Horace Walpole publica <em>El Castillo de Otranto</em>, inaugurando oficialmente el género de la novela gótica. Castillos medievales, fantasmas y misterio se vuelven elementos literarios centrales.</p>
        </div>
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="year">1800s — Literatura Oscura</div>
            <p>Edgar Allan Poe, Mary Shelley (<em>Frankenstein</em>, 1818) y Bram Stoker (<em>Drácula</em>, 1897) llevan la estética gótica a su cima literaria.</p>
        </div>
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="year">1979 — El Nacimiento</div>
            <p>Bauhaus lanza <em>Bela Lugosi's Dead</em>, considerada la primera canción del goth moderno. Post-punk inglés + atmósfera de horror cinematográfico = subcultura nueva.</p>
        </div>
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="year">1980 — El Batcave</div>
            <p>El club Batcave en Londres se convierte en el epicentro mundial de la subcultura gótica. Moda, música y actitud se fusionan en un espacio físico que define la identidad del movimiento.</p>
        </div>
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="year">1982 — La etiqueta</div>
            <p>El NME acuña el término "goth" para describir a bandas como The Cure y Siouxsie and the Banshees. La subcultura se expande a Alemania, EE.UU. y Japón.</p>
        </div>
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="year">1990s — Diversificación</div>
            <p>Nacen el Gothic Metal (Type O Negative, Paradise Lost) y el Industrial. El goth se fusiona con el dark ambient, el EBM y el ethereal wave.</p>
        </div>
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="year">Actualidad</div>
            <p>La cultura goth sigue evolucionando: TikTok Goth, nu-goth, witch house y darkwave revival. El southern gothic resurge como estética visual en cine, moda y fotografía.</p>
        </div>
    </div>
</section>

<!-- ══ MÚSICA ══ -->
<section id="musica">
    <p class="section-eyebrow">III — Sonido</p>
    <h2 class="section-title">Música y Bandas Fundacionales</h2>
    <p>Un sonido denso construido sobre guitarras reverberantes, bajos prominentes, cajas de ritmo frías y voces que oscilaban entre la angustia y el misticismo.</p>
    <div class="bands-grid">
        <div class="band-cell">
            <div class="band-name">Bauhaus</div>
            <div class="band-genre">Proto-Goth</div>
            <p>Los padres fundadores. Peter Murphy definió la estética vocal oscura que todo artista gótico heredó.</p>
        </div>
        <div class="band-cell">
            <div class="band-name">The Cure</div>
            <div class="band-genre">Post-Punk / Goth</div>
            <p>Robert Smith mezcló melancolía pop con oscuridad existencial. <em>Disintegration</em> (1989) es obra maestra del género.</p>
        </div>
        <div class="band-cell">
            <div class="band-name">Siouxsie & the Banshees</div>
            <div class="band-genre">Post-Punk / Goth</div>
            <p>Siouxsie Sioux definió la moda y el maquillaje del goth femenino. Influencia inestimable en la subcultura.</p>
        </div>
        <div class="band-cell">
            <div class="band-name">Joy Division</div>
            <div class="band-genre">Post-Punk</div>
            <p>Ian Curtis y su poesía desesperada. <em>Unknown Pleasures</em> es una de las portadas más icónicas del rock.</p>
        </div>
        <div class="band-cell">
            <div class="band-name">Sisters of Mercy</div>
            <div class="band-genre">Gothic Rock</div>
            <p>Andrew Eldritch combinó voces graves con una actitud nihilista. Su caja de ritmos "Doktor Avalanche" es legendaria.</p>
        </div>
        <div class="band-cell">
            <div class="band-name">Dead Can Dance</div>
            <div class="band-genre">Darkwave / Neoclásico</div>
            <p>Lisa Gerrard y Brendan Perry crearon un universo que mezcla música antigua, folk y oscuridad cinematográfica.</p>
        </div>
        <div class="band-cell">
            <div class="band-name">Nick Cave & the Bad Seeds</div>
            <div class="band-genre">Gothic Blues</div>
            <p>Donde el southern gothic se encuentra con la música. Violencia, religión y redención en letras inigualables.</p>
        </div>
        <div class="band-cell">
            <div class="band-name">Type O Negative</div>
            <div class="band-genre">Gothic Doom Metal</div>
            <p>Peter Steele llevó el goth al metal más denso y lento. Romanticismo oscuro y humor negro únicos.</p>
        </div>
        <div class="band-cell">
            <div class="band-name">Clan of Xymox</div>
            <div class="band-genre">Darkwave</div>
            <p>Banda holandesa que definió el darkwave europeo con sintetizadores melancólicos y texturas de sueño.</p>
        </div>
    </div>
    <div class="quote">
        "La música gótica toma prestado de todo: del punk su energía, del blues su dolor, del clasicismo su grandeza."
        <span class="quote-author">— Convergencia de influencias</span>
    </div>
</section>

<!-- ══ SUBCULTURAS ══ -->
<section id="subculturas">
    <p class="section-eyebrow">IV — Ramas</p>
    <h2 class="section-title">Subculturas Góticas</h2>
    <p>El goth nunca fue un movimiento monolítico. Desde sus primeros años evolucionó en múltiples ramas estéticas y filosóficas, cada una con su propio lenguaje visual y sonoro.</p>
    <div class="cards">
        <div class="card"><span class="card-icon">🖤</span><h3>Trad Goth</h3><p>El goth original. Cabello oscuro, maquillaje pálido y ropa post-punk. Pureza estética del movimiento fundacional.</p></div>
        <div class="card"><span class="card-icon">🕯</span><h3>Victorian Goth</h3><p>Funerales victorianos, romanticismo decadente, encajes, corsets y alta costura oscura. La muerte como ritual elegante.</p></div>
        <div class="card"><span class="card-icon">⚡</span><h3>Cybergoth</h3><p>Industrial + rave + futurismo distópico. Dreadlocks sintéticos, goggles, neon y estética post-apocalíptica.</p></div>
        <div class="card"><span class="card-icon">🌹</span><h3>Romantic Goth</h3><p>Emocional y poético. Influenciado por Keats y Byron. Rosas negras, castillos, cartas a la luz de las velas.</p></div>
        <div class="card"><span class="card-icon">🌿</span><h3>Witch Goth</h3><p>Naturaleza oscura, paganismo, brujería y espiritualidad femenina. Muy conectado con lo rural y lo ancestral.</p></div>
        <div class="card"><span class="card-icon">🎭</span><h3>Pastel Goth</h3><p>Contraste entre colores suaves y temáticas oscuras. Surgió en Japón fusionando kawaii con la estética mórbida.</p></div>
        <div class="card"><span class="card-icon">🏰</span><h3>Medieval Goth</h3><p>Inspirado en la Edad Media: armaduras, capas, misticismo pagano y neofolk. Muy cercano al folk oscuro.</p></div>
        <div class="card"><span class="card-icon">🎸</span><h3>Nu-Goth</h3><p>La versión contemporánea. Minimalista, urbano, con influencias del streetwear y el arte conceptual moderno.</p></div>
    </div>
</section>

<!-- ══ FIGURAS ══ -->
<section id="figuras">
    <p class="section-eyebrow">V — Iconos</p>
    <h2 class="section-title">Figuras Clave del Movimiento</h2>
    <p>La cultura gótica ha sido construida por artistas, escritores y músicos que le dieron forma y lenguaje a lo oscuro como territorio estético y filosófico.</p>
    <div class="figures-list">
        <div class="figure-row">
            <div><div class="figure-name">Edgar Allan Poe</div><div class="figure-date">1809 — 1849</div></div>
            <p>El padre literario de lo gótico americano. Sus cuentos de terror psicológico y su vida trágica lo convirtieron en el santo patrón del movimiento gótico moderno.</p>
        </div>
        <div class="figure-row">
            <div><div class="figure-name">Peter Murphy</div><div class="figure-date">Bauhaus, 1979</div></div>
            <p>Vocalista de Bauhaus. Su presencia escénica, sus pómulos pronunciados y su voz profunda definieron la imagen del "hombre gótico" por décadas.</p>
        </div>
        <div class="figure-row">
            <div><div class="figure-name">Siouxsie Sioux</div><div class="figure-date">1976 — presente</div></div>
            <p>La reina indiscutible del goth. Su maquillaje y cabello negro crearon el arquetipo de la mujer gótica que todavía persiste en la cultura popular global.</p>
        </div>
        <div class="figure-row">
            <div><div class="figure-name">Robert Smith</div><div class="figure-date">The Cure, 1976</div></div>
            <p>El hombre del cabello revuelto y el lápiz labial rojo. Combinó vulnerabilidad emocional con oscuridad existencial, haciendo del goth algo profundamente humano.</p>
        </div>
        <div class="figure-row">
            <div><div class="figure-name">Nick Cave</div><div class="figure-date">1983 — presente</div></div>
            <p>El poeta oscuro del southern gothic musical. Sus letras mezclan Biblia, violencia y redención en un universo que pertenece al goth y al blues del sur.</p>
        </div>
        <div class="figure-row">
            <div><div class="figure-name">Flannery O'Connor</div><div class="figure-date">1925 — 1964</div></div>
            <p>Escritora que definió el Southern Gothic literario. Sus personajes grotescos y su visión de la gracia en la violencia son centrales en esta tradición.</p>
        </div>
    </div>
</section>

<!-- ══ FILOSOFÍA ══ -->
<section id="filosofia">
    <p class="section-eyebrow">VI — Pensamiento</p>
    <h2 class="section-title">Filosofía Gótica</h2>
    <p>Más allá de la moda y la música, el goth es una actitud filosófica: una confrontación honesta con la oscuridad, la mortalidad y la belleza en lo imperfecto.</p>
    <div class="philosophy-grid">
        <div class="phil-item">
            <div class="phil-number">I</div>
            <h3>Memento Mori</h3>
            <p>Recuerda que morirás. El goth no huye de la muerte sino que la abraza como parte natural y bella de la existencia. La calavera es símbolo de humanidad compartida.</p>
        </div>
        <div class="phil-item">
            <div class="phil-number">II</div>
            <h3>Belleza en lo oscuro</h3>
            <p>El romanticismo negro encuentra arte en las ruinas, la decadencia y el abandono. Lo que el mundo llama feo, el goth lo ve como profundamente hermoso.</p>
        </div>
        <div class="phil-item">
            <div class="phil-number">III</div>
            <h3>Autenticidad</h3>
            <p>El goth rechaza el optimismo forzado y la superficialidad. Prefiere la honestidad emocional, incluso cuando conduce a lugares incómodos.</p>
        </div>
    </div>
    <div class="divider"><span>✟</span></div>
    <div class="quote">
        "Los góticos no son depresivos ni destructivos. Son personas que no temen mirar la oscuridad a los ojos y encontrar allí algo de valor."
        <span class="quote-author">— Sobre la subcultura</span>
    </div>
</section>

<!-- ══ CINE Y SERIES ══ -->
<section id="cine">
    <p class="section-eyebrow">VII — Pantalla</p>
    <h2 class="section-title">Cine y Series Góticas</h2>
    <p>El cine y la televisión han sido vehículos poderosos para la estética gótica, desde el expresionismo alemán hasta el southern gothic contemporáneo en streaming.</p>
    <div class="films-grid">
        <div class="film-card">
            <div class="film-year">1922</div>
            <div class="film-title">Nosferatu</div>
            <p>El vampiro como metáfora de lo extraño y lo monstruoso. F.W. Murnau crea la imagen vampírica que definiría un siglo de cine de horror.</p>
        </div>
        <div class="film-card">
            <div class="film-year">1994</div>
            <div class="film-title">Interview with the Vampire</div>
            <p>Brad Pitt y Tom Cruise en una exploración de la inmortalidad como condena. La estética gótica victoriana en todo su esplendor visual.</p>
        </div>
        <div class="film-card">
            <div class="film-year">2014</div>
            <div class="film-title">True Detective S1</div>
            <p>Rust Cohle y el nihilismo filosófico en los pantanos de Louisiana. Probablemente el ejemplo más puro de southern gothic en televisión moderna.</p>
        </div>
        <div class="film-card">
            <div class="film-year">2015</div>
            <div class="film-title">Crimson Peak</div>
            <p>Guillermo del Toro lleva el gothic romance victoriano a su máxima expresión visual. Mansiones, fantasmas y amor oscuro.</p>
        </div>
        <div class="film-card">
            <div class="film-year">2015</div>
            <div class="film-title">The Witch</div>
            <p>Horror folk en la Nueva Inglaterra puritana. Una familia se desintegra ante lo sobrenatural. Atmósfera agobiante y simbolismo religioso denso.</p>
        </div>
        <div class="film-card">
            <div class="film-year">2020</div>
            <div class="film-title">Midnight Mass</div>
            <p>Mike Flanagan explora fe, culpa y redención en una isla remota. Horror gótico que confronta la religión con lo sobrenatural sin resoluciones fáciles.</p>
        </div>
        <div class="film-card">
            <div class="film-year">2022</div>
            <div class="film-title">Wednesday</div>
            <p>La reinterpretación contemporánea del goth clásico para una nueva generación. Estética cuidada y guiños a toda la tradición del movimiento.</p>
        </div>
        <div class="film-card">
            <div class="film-year">2023</div>
            <div class="film-title">The Fall of the House of Usher</div>
            <p>Adaptación de Poe para el siglo XXI. Flanagan regresa al origen literario del gótico americano con una saga familiar sobre culpa y decadencia.</p>
        </div>
    </div>
</section>

<!-- ══ GALERÍA ══ -->
<div id="galeria">
    <div id="gallery">
        <div style="max-width:1100px; margin:0 auto;">
            <p class="section-eyebrow">VIII — Imágenes</p>
            <h2 class="section-title">Galería Atmosférica</h2>
        </div>
        <div class="gallery-grid">
            <div class="gallery-item" data-src="https://i.redd.it/w7nbjyjqpza51.jpg">
                <img src="https://i.redd.it/w7nbjyjqpza51.jpg" alt="Catedral Gótica" loading="lazy">
                <div class="gallery-caption">Catedral de Colonia · Arquitectura Gótica</div>
            </div>
            <div class="gallery-item" data-src="https://i0.wp.com/dovevado.net/wp-content/uploads/2018/09/P%C3%A8ere-Lachaise-1.jpg">
                <img src="https://i0.wp.com/dovevado.net/wp-content/uploads/2018/09/P%C3%A8ere-Lachaise-1.jpg" alt="Cementerio Père Lachaise" loading="lazy">
                <div class="gallery-caption">Père Lachaise · París</div>
            </div>
            <div class="gallery-item" data-src="https://medievalists.gumlet.io/wp-content/uploads/2018/04/whitby-abbey.jpg?compress=true&format=webp&quality=80&w=376&dpr=2.6">
                <img src="https://medievalists.gumlet.io/wp-content/uploads/2018/04/whitby-abbey.jpg?compress=true&format=webp&quality=80&w=376&dpr=2.6" alt="Abadía de Whitby" loading="lazy">
                <div class="gallery-caption">Abadía de Whitby · Inspiración de Drácula</div>
            </div>
            <div class="gallery-item" data-src="https://cdn.mos.cms.futurecdn.net/AhNpkJvfut2RVyWJEryZBm.jpg">
                <img src="https://cdn.mos.cms.futurecdn.net/AhNpkJvfut2RVyWJEryZBm.jpg" alt="Musgo del sur" loading="lazy">
                <div class="gallery-caption">Musgo Español · Southern Gothic</div>
            </div>
            <div class="gallery-item" data-src="https://images.fineartamerica.com/images-medium-large-5/notre-dame-at-night-karma-boyer.jpg">
                <img src="https://images.fineartamerica.com/images-medium-large-5/notre-dame-at-night-karma-boyer.jpg" alt="Notre Dame" loading="lazy">
                <div class="gallery-caption">Notre-Dame · Gárgolas y Arcos</div>
            </div>
        </div>
    </div>
</div>

<!-- ══ LIGHTBOX ══ -->
<div id="lightbox">
    <button id="lightbox-close">✕ CERRAR</button>
    <img id="lightbox-img" src="" alt="">
</div>

<!-- ══ SOUTHERN GOTHIC ══ -->
<section id="southern">
    <p class="section-eyebrow">IX — El Sur Oscuro</p>
    <h2 class="section-title">Southern Gothic</h2>
    <p>Una tradición literaria y artística del sur de Estados Unidos que mezcla la estética oscura con el paisaje sureño: iglesias abandonadas, pecados familiares, paisajes húmedos y una religiosidad que convive con lo grotesco.</p>
    <div class="sg-features">
        <div class="sg-feat"><h3>Paisaje</h3><p>Bosques de robles con musgo español, pantanos de Louisiana, campos de algodón abandonados y cementerios coloniales. La naturaleza como testigo de tragedias humanas.</p></div>
        <div class="sg-feat"><h3>Arquitectura</h3><p>Mansiones antebellum en ruinas, iglesias de madera, porches desvencijados. Estructuras que guardan memorias oscuras y secretos de generaciones pasadas.</p></div>
        <div class="sg-feat"><h3>Religión</h3><p>Una fe que convive con el pecado, la culpa y la violencia. Los predicadores ambulantes, los rituales del vudú y los rezos de madrugada forman el alma sureña oscura.</p></div>
        <div class="sg-feat"><h3>Folklore</h3><p>Espíritus del pantano, los Grunch Road Monsters de Nueva Orleans, rituales de magia folk hoodoo transmitidos por generaciones.</p></div>
        <div class="sg-feat"><h3>Literatura</h3><p>Flannery O'Connor, William Faulkner, Carson McCullers. Personajes marginales, familias disfuncionales y la gracia que llega a través del horror.</p></div>
        <div class="sg-feat"><h3>Música</h3><p>El blues del Delta, el gospel oscuro y el country murder ballad. Nick Cave y Tom Waits son los puentes entre el goth europeo y el alma del sur americano.</p></div>
    </div>
    <div class="quote">
        "Las capillas vacías y los caminos cubiertos de niebla se volvieron símbolos del alma gótica sureña. La decadencia no como fracaso, sino como memoria."
        <span class="quote-author">— Southern Gothic</span>
    </div>
</section>

<!-- ══ FOOTER ══ -->
<footer>
    <div class="footer-logo candle-slow">✦ SOUTHERN GOTH ✦</div>
    <p class="footer-text">Historia de la Cultura Gótica · Por Mery C.E.</p>
</footer>

<!-- ══ SOUNDCLOUD OCULTO ══ -->
<iframe id="sc-iframe" width="0" height="0" style="display:none;"
    scrolling="no" frameborder="no" allow="autoplay"
    src="https://w.soundcloud.com/player/?url=https%3A//soundcloud.com/havocharpa/detuned-mini-bass&color=%236e7857&auto_play=true&hide_related=true&show_comments=false&show_user=false&show_reposts=false&show_teaser=false">
</iframe>

<!-- ══ MUSIC PLAYER ══ -->
<div id="music-player">
    <span id="music-icon">♪</span>
    <div>
        <div id="music-title">Detuned Mini Bass</div>
        <div id="music-artist">HavocHarpa</div>
    </div>
    <button id="music-toggle">⏸</button>
</div>

<!-- ══ SCRIPTS ══ -->
<script>
/* ── LOADER ── */
window.addEventListener('load', () => {
    setTimeout(() => {
        document.getElementById('loader').classList.add('hidden');
    }, 2200);
});

/* ── SCROLL REVEAL ── */
const revealEls = document.querySelectorAll('section, #rotating-quotes, #gallery');
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => { if(e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.07 });
revealEls.forEach(el => revealObserver.observe(el));

/* ── PARALLAX HERO ── */
window.addEventListener('scroll', () => {
    const bg = document.querySelector('.hero-bg');
    const s = window.scrollY;
    if(bg && s < window.innerHeight)
        bg.style.transform = `scale(1.07) translateY(${s * 0.14}px)`;
});

/* ── PROGRESS DOTS ── */
const sections = ['hero','origen','cronologia','musica','subculturas','figuras','filosofia','cine','galeria','southern'];
const dots = document.querySelectorAll('.prog-dot');

function updateDots() {
    let current = 0;
    sections.forEach((id, i) => {
        const el = document.getElementById(id);
        if(el) {
            const rect = el.getBoundingClientRect();
            if(rect.top <= window.innerHeight * 0.5) current = i;
        }
    });
    dots.forEach((d, i) => d.classList.toggle('active', i === current));
}

window.addEventListener('scroll', updateDots, { passive: true });

dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
        const el = document.getElementById(sections[i]);
        if(el) el.scrollIntoView({ behavior:'smooth' });
    });
});

/* ── CITAS ROTATIVAS ── */
const quotes = [
    { text: "Nunca fue sobre la muerte. Siempre fue sobre encontrar belleza en lo que el mundo descarta.", author: "— Subcultura Gótica" },
    { text: "En el sur, hasta los fantasmas tienen modales.", author: "— Flannery O'Connor" },
    { text: "El negro no es la ausencia de color, es la presencia de todos ellos a la vez.", author: "— Estética Gótica" },
    { text: "La oscuridad tiene su propia clase de libertad.", author: "— Nick Cave" },
    { text: "Los mejores cuentos de terror no tratan sobre monstruos. Tratan sobre la naturaleza humana.", author: "— Edgar Allan Poe" },
    { text: "Las capillas vacías y los caminos cubiertos de niebla se volvieron símbolos del alma gótica sureña.", author: "— Southern Gothic" },
    { text: "Hay belleza en la decadencia. Una rosa marchita todavía tiene más alma que una flor de plástico.", author: "— Romanticismo Oscuro" }
];

const rqText  = document.querySelector('.rq-text');
const rqAuth  = document.querySelector('.rq-author');
const rqDots  = document.querySelector('.rq-dots');
let currentQ  = 0;

// Crear dots
quotes.forEach((_, i) => {
    const d = document.createElement('div');
    d.className = 'rq-dot' + (i === 0 ? ' active' : '');
    d.addEventListener('click', () => goToQuote(i));
    rqDots.appendChild(d);
});

function goToQuote(idx) {
    rqText.classList.add('fade');
    rqAuth.classList.add('fade');
    setTimeout(() => {
        currentQ = idx;
        rqText.textContent = quotes[idx].text;
        rqAuth.textContent = quotes[idx].author;
        rqText.classList.remove('fade');
        rqAuth.classList.remove('fade');
        document.querySelectorAll('.rq-dot').forEach((d,i) => d.classList.toggle('active', i===idx));
    }, 700);
}

goToQuote(0);
setInterval(() => goToQuote((currentQ + 1) % quotes.length), 6000);

/* ── GALERÍA LIGHTBOX ── */
const galleryItems = document.querySelectorAll('.gallery-item');
const lightbox = document.getElementById('lightbox');
const lbImg = document.getElementById('lightbox-img');

galleryItems.forEach(item => {
    item.addEventListener('click', () => {
        const src = item.dataset.src || item.querySelector('img').src;
        lbImg.src = src;
        lightbox.classList.add('open');
    });
});

document.getElementById('lightbox-close').addEventListener('click', () => lightbox.classList.remove('open'));
lightbox.addEventListener('click', (e) => { if(e.target === lightbox) lightbox.classList.remove('open'); });
document.addEventListener('keydown', (e) => { if(e.key === 'Escape') lightbox.classList.remove('open'); });

/* ── SOUNDCLOUD PLAYER ── */
const iframe = document.getElementById('sc-iframe');
const toggleBtn = document.getElementById('music-toggle');
const player = document.getElementById('music-player');
let isPlaying = true;

const scScript = document.createElement('script');
scScript.src = 'https://w.soundcloud.com/player/api.js';
scScript.onload = () => {
    const widget = SC.Widget(iframe);
    toggleBtn.addEventListener('click', () => {
        if(isPlaying) {
            widget.pause();
            toggleBtn.textContent = '▶';
            player.classList.add('paused');
        } else {
            widget.play();
            toggleBtn.textContent = '⏸';
            player.classList.remove('paused');
        }
        isPlaying = !isPlaying;
    });
};
document.body.appendChild(scScript);
</script>

</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run()
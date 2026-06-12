
"""
EmoBridge - Autism Support App for Children
════════════════════════════════════════════
Resolution : 320 × 480 px  (locked for 3.5-inch robot screen)
Framework  : PyQt5
Structure  :
    § 1  — Constants & asset helpers
    § 2  — Shared UI widgets  (AnimatedBG, WaveHeader, GlassCard, GradientButton,
                               HeartsWidget, FullScreenEmojiOverlay)
    § 3  — Screens            (OnboardingScreen, HomeScreen, GameSelectionScreen,
                               EmojiGameScreen, ColorFeelingsGame,
                               ProgressScreen, ThemeScreen)
    § 4  — App controller     (EmoBridgeApp)
    § 5  — Entry point
"""

import sys 
import os 
import math 
import random 
import datetime 
import sqlite3 
from PyQt5 .QtWidgets import QGraphicsOpacityEffect ,QDialog 
from PyQt5 .QtCore import Qt 

try :
    from backend import add_child ,search_child ,add_session ,add_game_result 
except ImportError :

    def add_child (name ,age ,avatar ,theme ):
        pass 
    def search_child (name ):
        return (1 ,name ,7 ,"Avatar_Default","Default")
    def add_session (**kwargs ):
        pass 
    def add_game_result (**kwargs ):
        pass 

from PyQt5 .QtWidgets import (
QApplication ,QMainWindow ,QWidget ,QVBoxLayout ,QHBoxLayout ,
QLabel ,QPushButton ,QLineEdit ,QStackedWidget ,QFrame ,
QGraphicsDropShadowEffect ,QScrollArea ,QSizePolicy ,QSpinBox ,
QProgressBar ,QGridLayout ,QDialog 
)
from PyQt5 .QtCore import (
Qt ,QTimer ,QPropertyAnimation ,QEasingCurve ,QPoint ,QRect ,
QSequentialAnimationGroup ,QParallelAnimationGroup ,QSize ,
pyqtProperty ,QObject ,pyqtSignal ,QThread 
)
from PyQt5 .QtGui import (
QPainter ,QColor ,QFont ,QLinearGradient ,QRadialGradient ,
QPainterPath ,QBrush ,QPen ,QPixmap ,QImage ,QFontDatabase ,
QIcon ,QRegion ,QPalette ,QMovie 
)






APP_W ,APP_H =480 ,320 


CURRENT_CHILD_ID :int |None =None 
GAME_START_TIME :str |None =None 
TOTAL_ATTEMPTS =0 
SUCCESSFUL_ATTEMPTS =0 
DISTRACTION_COUNT =0 
DOMINANT_EMOTION ="Neutral"
FINAL_ENGAGEMENT =0.0 

BASE_DIR =os .path .dirname (os .path .abspath (__file__ ))
ASSETS_DIR =os .path .join (BASE_DIR ,"assets")


ASSET_BACKGROUND ="background.png"
ASSET_LOGO ="logo.png"
ASSET_LOGO_FULL ="logo_full.png"
ASSET_LEVELS =["level_1.png","level_2.png","level_3.png","level_4.png"]
ASSET_AVATARS =[f"avatar_{i }.png"for i in range (1 ,9 )]
AVATAR_NAMES =[
"Robot Friend","Gentle Elephant","Puzzle Bear","Friendly Cat",
"Brave Lion","Thoughtful Owl","Galaxy Whale","Super Monkey",
]


def asset_path (filename :str )->str :
    """Return the full path for an asset filename."""
    return os .path .join (ASSETS_DIR ,filename )


def load_pixmap (filename :str ,w :int =None ,h :int =None ,
keep_aspect :bool =True )->QPixmap :
    """Load a pixmap from assets/ with optional high-quality scaling."""
    path =asset_path (filename )
    if not os .path .exists (path ):
        return QPixmap ()
    pix =QPixmap (path )
    if pix .isNull ()or w is None or h is None :
        return pix 
    mode =Qt .KeepAspectRatio if keep_aspect else Qt .IgnoreAspectRatio 
    return pix .scaled (w ,h ,mode ,Qt .SmoothTransformation )


def load_pixmap_fit (filename :str ,w :int ,h :int )->QPixmap :
    """Scale image to fit w×h without cropping."""
    path =asset_path (filename )
    if not os .path .exists (path ):
        return QPixmap ()
    pix =QPixmap (path )
    if pix .isNull ():
        return pix 
    return pix .scaled (w ,h ,Qt .KeepAspectRatio ,Qt .SmoothTransformation )


def get_background_themes ()->list [str ]:
    """
    Return all background*.png files found in assets/, sorted so that
    background.png comes first, then background2.png, background3.png …
    يمكنك إضافة صور خلفية جديدة بأسماء: background2.png, background3.png …
    """
    bg_files :list [str ]=[]
    if os .path .exists (ASSETS_DIR ):
        for f in os .listdir (ASSETS_DIR ):
            if f .startswith ("background")and f .endswith (".png"):
                bg_files .append (f )

    def _sort_key (name ):
        if name =="background.png":
            return (0 ,0 )
        num ="".join (c for c in name if c .isdigit ())
        return (1 ,int (num )if num else 9999 )

    bg_files .sort (key =_sort_key )
    return bg_files or ["background.png"]


def _get_latest_session_id ()->int :
    """Return the latest session_id from SQLite (helper for DB integration)."""
    try :
        conn =sqlite3 .connect ("emobridge.db")
        cursor =conn .cursor ()
        cursor .execute ("SELECT max(session_id) FROM sessions")
        res =cursor .fetchone ()
        conn .close ()
        return res [0 ]if res and res [0 ]else 1 
    except Exception :
        return 1 


def _save_game_result (score :int ,game_name :str ="Unknown")->None :
    """
    Save session + game result to DB.
    استخدم هذي الدالة في نهاية كل لعبة بدل تكرار الكود.
    """
    global CURRENT_CHILD_ID ,GAME_START_TIME ,TOTAL_ATTEMPTS ,SUCCESSFUL_ATTEMPTS ,DISTRACTION_COUNT ,DOMINANT_EMOTION ,FINAL_ENGAGEMENT 
    end_time =datetime .datetime .now ().strftime ("%Y-%m-%d %H:%M:%S")
    start_time =GAME_START_TIME or end_time 
    total =max (TOTAL_ATTEMPTS ,1 )
    success_rate =(SUCCESSFUL_ATTEMPTS /total *100 )if total >0 else 0 

    try :
        add_session (
        child_id =CURRENT_CHILD_ID or 1 ,
        start_time =start_time ,
        end_time =end_time ,
        dominant_emotion =DOMINANT_EMOTION ,
        avg_confidence =85.0 ,
        engagement_rate =FINAL_ENGAGEMENT ,
        distraction_count =DISTRACTION_COUNT ,
        )

        session_id =_get_latest_session_id ()
        add_game_result (
        session_id =session_id ,
        score =score ,
        difficulty_level ="Normal",
        total_attempts =total ,
        success_rate =success_rate ,
        reaction_time =1.8 ,
        )
    except Exception :
        pass 





from PyQt5 .QtCore import QPropertyAnimation ,QEasingCurve ,QRect 

class WinCelebrationDialog (QDialog ):
    def __init__ (self ,parent =None ,xp_earned =50 ):
        super ().__init__ (parent )
        self .setWindowFlags (Qt .FramelessWindowHint |Qt .WindowSystemMenuHint )
        self .setAttribute (Qt .WA_TranslucentBackground )
        self .setFixedSize (480 ,320 )

        self .xp_earned =xp_earned 
        self ._setup_ui ()

    def _setup_ui (self ):

        self .bg_overlay =QWidget (self )
        self .bg_overlay .setGeometry (0 ,0 ,480 ,320 )
        self .bg_overlay .setStyleSheet ("background-color: rgba(15, 23, 42, 0.45);")


        self .card =GlassCard (self ,radius =24 )
        self .card .setFixedSize (300 ,220 )


        self .card .move (90 ,-230 )


        layout =QVBoxLayout (self .card )
        layout .setContentsMargins (15 ,15 ,15 ,15 )
        layout .setSpacing (10 )
        layout .setAlignment (Qt .AlignCenter )


        self .icon_lbl =QLabel ("🎉🏆🎉",self .card )
        self .icon_lbl .setStyleSheet ("font-size: 36px; background: transparent;")
        self .icon_lbl .setAlignment (Qt .AlignCenter )
        layout .addWidget (self .icon_lbl )


        self .title_lbl =QLabel ("YOU WIN!",self .card )
        self .title_lbl .setStyleSheet ("""
            font-family: 'Segoe UI', Arial; font-size: 22px; font-weight: 900; 
            color: #10b981; background: transparent;
        """)
        self .title_lbl .setAlignment (Qt .AlignCenter )
        layout .addWidget (self .title_lbl )


        self .xp_lbl =QLabel (f"+{self .xp_earned } XP EARNED! ⭐",self .card )
        self .xp_lbl .setStyleSheet ("""
            font-size: 14px; font-weight: 800; color: #7c3aed; 
            background: rgba(124, 58, 237, 0.1); padding: 4px 12px; border-radius: 10px;
        """)
        self .xp_lbl .setAlignment (Qt .AlignCenter )
        layout .addWidget (self .xp_lbl ,alignment =Qt .AlignHCenter )

        layout .addSpacing (5 )


        self .continue_btn =QPushButton ("Awesome! ✨",self .card )
        self .continue_btn .setFixedSize (160 ,38 )
        self .continue_btn .setCursor (Qt .PointingHandCursor )
        self .continue_btn .setStyleSheet ("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #059669);
                color: white; border: none; border-radius: 19px; font-size: 13px; font-weight: 800;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #34d399, stop:1 #10b981);
            }
            QPushButton:pressed { padding-top: 2px; }
        """)
        self .continue_btn .clicked .connect (self .accept )
        layout .addWidget (self .continue_btn ,alignment =Qt .AlignHCenter )

    def exec_ (self ):

        self .anim =QPropertyAnimation (self .card ,b"geometry")
        self .anim .setDuration (600 )
        self .anim .setStartValue (QRect (90 ,-230 ,300 ,220 ))
        self .anim .setEndValue (QRect (90 ,50 ,300 ,220 ))

        self .anim .setEasingCurve (QEasingCurve .OutBounce )
        self .anim .start ()

        return super ().exec_ ()
class AnimatedBG (QWidget ):
    """
    Full-screen animated background: image or gradient fallback,
    with twinkling stars, floating clouds, and soft orbs.
    """

    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        self .setFixedSize (APP_W ,APP_H )
        self ._bg_pixmap =load_pixmap (ASSET_BACKGROUND ,APP_W ,APP_H ,keep_aspect =False )
        if self ._bg_pixmap .isNull ():
            self ._bg_pixmap =None 



        self .clouds =[]

        for _ in range (4 ):
            self .clouds .append ({
            "x":random .uniform (-80 ,APP_W +40 ),
            "y_base":random .uniform (20 ,90 ),
            "y":0.0 ,
            "vx":random .uniform (0.10 ,0.18 ),
            "w":random .randint (55 ,85 ),
            "alpha":random .randint (80 ,120 ),
            "layer":0 ,
            "drift_amp":2.5 ,
            "drift_spd":0.006 ,
            "drift_phase":random .uniform (0 ,6.28 ),
            })

        for _ in range (3 ):
            self .clouds .append ({
            "x":random .uniform (-100 ,APP_W +60 ),
            "y_base":random .uniform (100 ,165 ),
            "y":0.0 ,
            "vx":random .uniform (0.20 ,0.32 ),
            "w":random .randint (80 ,120 ),
            "alpha":random .randint (140 ,190 ),
            "layer":1 ,
            "drift_amp":3.5 ,
            "drift_spd":0.009 ,
            "drift_phase":random .uniform (0 ,6.28 ),
            })

        for _ in range (2 ):
            self .clouds .append ({
            "x":random .uniform (-120 ,APP_W +80 ),
            "y_base":random .uniform (195 ,245 ),
            "y":0.0 ,
            "vx":random .uniform (0.35 ,0.50 ),
            "w":random .randint (110 ,150 ),
            "alpha":random .randint (195 ,240 ),
            "layer":2 ,
            "drift_amp":4.5 ,
            "drift_spd":0.012 ,
            "drift_phase":random .uniform (0 ,6.28 ),
            })


        self .stars =[
        {"x":random .uniform (4 ,APP_W -4 ),"y":random .uniform (6 ,APP_H *0.65 ),
        "phase":random .uniform (0 ,6.28 ),"size":random .uniform (2.5 ,6.5 ),
        "speed":random .uniform (0.025 ,0.065 ),"warm":random .choice ([True ,False ])}
        for _ in range (22 )
        ]


        self .orbs =[
        {"x":random .uniform (0 ,APP_W ),"y":random .uniform (20 ,APP_H ),
        "vy":random .uniform (-0.05 ,-0.22 ),"vx":random .uniform (-0.03 ,0.03 ),
        "r":random .uniform (2.0 ,5.5 ),
        "phase":random .uniform (0 ,6.28 ),"hue":random .choice (["teal","purple","pink"])}
        for _ in range (12 )
        ]


        self .dust =[
        {"x":random .uniform (0 ,APP_W ),"y":random .uniform (0 ,APP_H ),
        "vy":random .uniform (-0.10 ,-0.03 ),"vx":random .uniform (-0.04 ,0.04 ),
        "phase":random .uniform (0 ,6.28 ),"size":random .uniform (0.8 ,2.0 )}
        for _ in range (22 )
        ]

        self .tick =0 
        self ._timer =QTimer (self )
        self ._timer .timeout .connect (self ._animate )
        self ._timer .start (16 )


    def set_background_image (self ,filename :str )->None :
        """Swap background image at runtime (called from ThemeScreen)."""
        self ._bg_pixmap =load_pixmap (filename ,APP_W ,APP_H ,keep_aspect =False )
        if self ._bg_pixmap .isNull ():
            self ._bg_pixmap =None 
        self .update ()


    def _animate (self ):
        self .tick +=1 
        t =self .tick 
        for c in self .clouds :
            c ["x"]+=c ["vx"]

            c ["y"]=c ["y_base"]+c ["drift_amp"]*math .sin (c ["drift_phase"]+t *c ["drift_spd"])
            c ["drift_phase"]+=0.005 

            exit_w =c ["w"]+20 
            if c ["x"]>APP_W +exit_w :
                c ["x"]=-exit_w 
        for o in self .orbs :
            o ["y"]+=o ["vy"]
            o ["x"]+=o ["vx"]
            if o ["y"]<-12 :
                o ["y"]=APP_H +12 
                o ["x"]=random .uniform (0 ,APP_W )
            if o ["x"]<-12 :o ["x"]=APP_W +12 
            if o ["x"]>APP_W +12 :o ["x"]=-12 
        for d in self .dust :
            d ["y"]+=d ["vy"]
            d ["x"]+=d ["vx"]
            if d ["y"]<-6 :
                d ["y"]=APP_H +6 
                d ["x"]=random .uniform (0 ,APP_W )
        self .update ()

    def paintEvent (self ,event ):
        p =QPainter (self )
        p .setRenderHint (QPainter .Antialiasing )
        p .setRenderHint (QPainter .SmoothPixmapTransform )


        if self ._bg_pixmap and not self ._bg_pixmap .isNull ():
            p .drawPixmap (0 ,0 ,self ._bg_pixmap )
        else :
            grad =QLinearGradient (0 ,0 ,0 ,APP_H )
            grad .setColorAt (0.0 ,QColor (145 ,210 ,245 ))
            grad .setColorAt (0.45 ,QColor (190 ,175 ,238 ))
            grad .setColorAt (1.0 ,QColor (165 ,135 ,220 ))
            p .fillRect (0 ,0 ,APP_W ,APP_H ,grad )


        overlay =QLinearGradient (0 ,0 ,0 ,APP_H )
        overlay .setColorAt (0.0 ,QColor (120 ,180 ,255 ,15 ))
        overlay .setColorAt (1.0 ,QColor (90 ,60 ,160 ,18 ))
        p .fillRect (0 ,0 ,APP_W ,APP_H ,overlay )


        for s in self .stars :
            phase =s ["phase"]+self .tick *s ["speed"]
            pulse =0.55 +0.45 *math .sin (phase )
            alpha =int (100 +120 *pulse )
            sz =s ["size"]*(0.75 +0.35 *pulse )
            cx ,cy =s ["x"],s ["y"]
            if s ["warm"]:
                core =QColor (255 ,248 ,210 ,alpha )
                glow =QColor (255 ,220 ,140 ,alpha //4 )
            else :
                core =QColor (220 ,240 ,255 ,alpha )
                glow =QColor (180 ,210 ,255 ,alpha //4 )
            p .setPen (Qt .NoPen )
            p .setBrush (QBrush (glow ))
            p .drawEllipse (int (cx -sz *1.3 ),int (cy -sz *1.3 ),int (sz *2.6 ),int (sz *2.6 ))
            p .setPen (QPen (core ,1.0 ))
            p .setBrush (QBrush (core ))
            sz2 =sz *0.40 
            p .drawLine (int (cx -sz ),int (cy ),int (cx +sz ),int (cy ))
            p .drawLine (int (cx ),int (cy -sz ),int (cx ),int (cy +sz ))
            p .drawLine (int (cx -sz2 ),int (cy -sz2 ),int (cx +sz2 ),int (cy +sz2 ))
            p .drawLine (int (cx -sz2 ),int (cy +sz2 ),int (cx +sz2 ),int (cy -sz2 ))


        for o in self .orbs :
            pulse =0.5 +0.5 *math .sin (o ["phase"]+self .tick *0.030 )
            alpha =int (22 +45 *pulse )
            hue =o ["hue"]
            if hue =="teal":col =QColor (39 ,193 ,214 ,alpha )
            elif hue =="purple":col =QColor (167 ,139 ,250 ,alpha )
            else :col =QColor (244 ,114 ,182 ,alpha )
            p .setPen (Qt .NoPen )
            r =o ["r"]*(0.80 +0.28 *pulse )
            rg =QRadialGradient (o ["x"],o ["y"],r *1.7 )
            glow_c =QColor (col );glow_c .setAlpha (alpha //4 )
            rg .setColorAt (0.0 ,col );rg .setColorAt (1.0 ,glow_c )
            p .setBrush (QBrush (rg ))
            p .drawEllipse (int (o ["x"]-r *1.7 ),int (o ["y"]-r *1.7 ),int (r *3.4 ),int (r *3.4 ))


        for d in self .dust :
            pulse =0.5 +0.5 *math .sin (d ["phase"]+self .tick *0.055 )
            alpha =int (30 +75 *pulse )
            sz =d ["size"]*(0.7 +0.45 *pulse )
            p .setPen (Qt .NoPen )
            p .setBrush (QBrush (QColor (255 ,255 ,255 ,alpha )))
            p .drawEllipse (int (d ["x"]-sz ),int (d ["y"]-sz ),int (sz *2 ),int (sz *2 ))


        for c in sorted (self .clouds ,key =lambda c :c ["layer"]):
            self ._draw_cloud (p ,c ["x"],c ["y"],c ["w"],c ["alpha"])
        p .end ()

    def _draw_cloud (self ,p :QPainter ,x :float ,y :float ,w :float ,alpha :int ):
        """
        Draw a clean, fluffy cloud made of overlapping soft circles.
        Uses a single unified QPainterPath so there are no visible seams.
        """
        h =w *0.40 


        puffs =[
        (x +w *0.00 ,y +h *0.35 ,w *0.38 ,h *0.72 ),
        (x +w *0.20 ,y +h *0.05 ,w *0.40 ,h *0.90 ),
        (x +w *0.42 ,y +h *0.00 ,w *0.36 ,h *1.00 ),
        (x +w *0.60 ,y +h *0.12 ,w *0.34 ,h *0.85 ),
        (x +w *0.76 ,y +h *0.30 ,w *0.28 ,h *0.72 ),
        ]

        path =QPainterPath ()


        path .setFillRule (Qt .WindingFill )

        for px ,py ,pw ,ph in puffs :
            path .addEllipse (px ,py ,pw ,ph )


        base_y =y +h *0.70 
        path .addRect (x ,base_y ,w *1.05 ,h *0.40 )


        cx =x +w *0.50 
        cy =y +h *0.35 
        rg =QRadialGradient (cx ,cy ,w *0.65 )
        rg .setColorAt (0.00 ,QColor (255 ,255 ,255 ,min (255 ,alpha +30 )))
        rg .setColorAt (0.55 ,QColor (252 ,253 ,255 ,alpha ))
        rg .setColorAt (1.00 ,QColor (225 ,238 ,255 ,max (0 ,alpha -70 )))

        p .setPen (Qt .NoPen )
        p .setBrush (QBrush (rg ))
        p .drawPath (path )


class WaveHeader (QWidget ):
    """Animated wave header with sparkles."""

    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        self .setFixedSize (APP_W ,72 )
        self .setAttribute (Qt .WA_TranslucentBackground )
        self ._phase =0.0 
        self ._sparkles =[
        {"t":random .uniform (0 ,1 ),"sp":random .uniform (0.5 ,1.2 ),
        "r":random .uniform (1.5 ,3 )}
        for _ in range (12 )
        ]
        timer =QTimer (self );timer .timeout .connect (self ._tick );timer .start (30 )

    def _tick (self ):
        self ._phase +=0.045 
        self .update ()

    def _wave_y (self ,t ,base_y ,amplitude ,freq =1.0 ,phase_off =0.0 ):
        return (base_y 
        +amplitude *math .sin (self ._phase +phase_off +t *math .pi *2.2 *freq )
        +amplitude *0.3 *math .sin (self ._phase *1.3 +phase_off *0.7 +t *math .pi *3.5 *freq ))

    def paintEvent (self ,event ):
        p =QPainter (self )
        p .setRenderHint (QPainter .Antialiasing )
        steps =64 

        path =QPainterPath ()
        path .moveTo (0 ,0 );path .lineTo (APP_W ,0 )
        for i in range (steps ,-1 ,-1 ):
            t =i /steps 
            path .lineTo (t *APP_W ,self ._wave_y (t ,38 ,7 ))
        path .closeSubpath ()

        p .setPen (Qt .NoPen )
        hg =QLinearGradient (0 ,0 ,0 ,50 )
        hg .setColorAt (0.0 ,QColor (255 ,255 ,255 ,215 ))
        hg .setColorAt (0.55 ,QColor (255 ,255 ,255 ,160 ))
        hg .setColorAt (1.0 ,QColor (255 ,255 ,255 ,0 ))
        p .setBrush (QBrush (hg ));p .drawPath (path )

        glow =QLinearGradient (0 ,36 ,0 ,58 )
        glow .setColorAt (0 ,QColor (39 ,193 ,214 ,38 ));glow .setColorAt (1 ,QColor (39 ,193 ,214 ,0 ))
        p .setBrush (QBrush (glow ));p .drawRect (0 ,36 ,APP_W ,22 )

        def draw_wave_line (base_y ,amp ,color ,width ,freq =1.0 ,phase_off =0.0 ):
            pen =QPen (color ,width );pen .setCapStyle (Qt .RoundCap );p .setPen (pen )
            wp =QPainterPath ()
            for i in range (steps +1 ):
                t =i /steps ;x =t *APP_W ;y =self ._wave_y (t ,base_y ,amp ,freq ,phase_off )
                wp .moveTo (x ,y )if i ==0 else wp .lineTo (x ,y )
            p .drawPath (wp )

        draw_wave_line (40 ,6 ,QColor (39 ,193 ,214 ,220 ),3.0 )
        draw_wave_line (46 ,5 ,QColor (138 ,92 ,210 ,180 ),2.4 ,freq =1.15 ,phase_off =0.7 )
        draw_wave_line (52 ,3.5 ,QColor (103 ,225 ,229 ,130 ),1.8 ,freq =1.3 ,phase_off =1.4 )

        p .setPen (Qt .NoPen )
        for sp in self ._sparkles :
            t =(sp ["t"]+self ._phase *0.02 *sp ["sp"])%1.0 
            x =t *APP_W 
            y =self ._wave_y (t ,40 ,6 )-4 
            pulse =0.55 +0.45 *math .sin (self ._phase *2.5 +sp ["sp"]*3 )
            alpha =int (100 +125 *pulse )
            p .setBrush (QBrush (QColor (255 ,255 ,255 ,alpha )))
            r =sp ["r"]*(0.8 +0.35 *pulse )
            p .drawEllipse (int (x -r ),int (y -r ),int (r *2 ),int (r *2 ))
        p .end ()


class GlassCard (QWidget ):
    """Semi-transparent frosted glass card."""

    def __init__ (self ,parent =None ,radius =18 ):
        super ().__init__ (parent )
        self ._radius =radius 
        self .setAttribute (Qt .WA_TranslucentBackground )

    def paintEvent (self ,event ):
        p =QPainter (self );p .setRenderHint (QPainter .Antialiasing )
        rect =self .rect ()
        path =QPainterPath ()
        path .addRoundedRect (rect .x (),rect .y (),rect .width (),rect .height (),
        self ._radius ,self ._radius )
        p .setPen (QPen (QColor (255 ,255 ,255 ,120 ),1.5 ))
        p .setBrush (QBrush (QColor (255 ,255 ,255 ,170 )))
        p .drawPath (path );p .end ()


class GradientButton (QPushButton ):
    """Animated gradient button with emoji icon and arrow."""

    BTN_W =195 ;BTN_H =56 ;RADIUS =16 

    def __init__ (self ,text ,emoji ,colors ,parent =None ):
        super ().__init__ (parent )
        self ._text =text ;self ._emoji =emoji ;self ._colors =colors 
        self ._hover =False ;self ._pressed =False ;self ._scale =1.0 
        self .setFixedSize (self .BTN_W ,self .BTN_H )
        self .setCursor (Qt .PointingHandCursor )
        self .setAttribute (Qt .WA_TranslucentBackground )
        self .setFlat (True )
        self ._anim =QPropertyAnimation (self ,b"scale_factor")
        self ._anim .setDuration (150 )
        self ._anim .setEasingCurve (QEasingCurve .OutBounce )

    def get_scale (self ):return self ._scale 
    def set_scale (self ,v ):self ._scale =v ;self .update ()
    scale_factor =pyqtProperty (float ,get_scale ,set_scale )

    def enterEvent (self ,e ):self ._hover =True ;self .update ()
    def leaveEvent (self ,e ):self ._hover =False ;self .update ()

    def mousePressEvent (self ,e ):
        self ._pressed =True 
        self ._anim .setStartValue (1.0 );self ._anim .setEndValue (0.94 );self ._anim .start ()
        super ().mousePressEvent (e )

    def mouseReleaseEvent (self ,e ):
        self ._pressed =False 
        self ._anim .setStartValue (0.94 );self ._anim .setEndValue (1.0 );self ._anim .start ()
        super ().mouseReleaseEvent (e )

    def paintEvent (self ,event ):
        p =QPainter (self );p .setRenderHint (QPainter .Antialiasing )
        w ,h =self .width (),self .height ();cx ,cy =w /2 ,h /2 ;r =self .RADIUS 

        p .translate (cx ,cy );p .scale (self ._scale ,self ._scale );p .translate (-cx ,-cy )

        shadow_c =QColor (self ._colors [0 ]);shadow_c .setAlpha (50 )
        p .setPen (Qt .NoPen );p .setBrush (QBrush (shadow_c ))
        p .drawRoundedRect (4 ,4 ,w -8 ,h -6 ,r ,r )

        grad =QLinearGradient (0 ,0 ,w ,0 )
        c0 =QColor (self ._colors [0 ]);c1 =QColor (self ._colors [1 ])
        if self ._hover :c0 =c0 .lighter (112 );c1 =c1 .lighter (112 )
        grad .setColorAt (0 ,c0 );grad .setColorAt (1 ,c1 )
        p .setBrush (QBrush (grad ));p .setPen (QPen (QColor (255 ,255 ,255 ,220 ),2.5 ))
        p .drawRoundedRect (1 ,1 ,w -2 ,h -3 ,r ,r )

        sheen =QLinearGradient (0 ,2 ,0 ,h //2 )
        sheen .setColorAt (0 ,QColor (255 ,255 ,255 ,70 ));sheen .setColorAt (1 ,QColor (255 ,255 ,255 ,0 ))
        p .setPen (Qt .NoPen );p .setBrush (QBrush (sheen ))
        p .drawRoundedRect (3 ,3 ,w -6 ,(h -6 )//2 ,r -2 ,r -2 )


        p .setBrush (QBrush (QColor (255 ,255 ,255 ,60 )))
        p .setPen (QPen (QColor (255 ,255 ,255 ,180 ),1.5 ))
        p .drawEllipse (10 ,(h -38 )//2 ,38 ,38 )
        p .setPen (QColor (255 ,255 ,255 ))
        p .setFont (QFont ("Segoe UI Emoji",18 ))
        p .drawText (QRect (10 ,(h -38 )//2 ,38 ,38 ),Qt .AlignCenter ,self ._emoji )


        p .setPen (QColor (255 ,255 ,255 ))
        p .setFont (QFont ("Segoe UI",13 ,QFont .Weight .Bold ))
        p .drawText (QRect (54 ,0 ,w -78 ,h ),Qt .AlignVCenter |Qt .AlignLeft ,self ._text )


        p .setBrush (QBrush (QColor (255 ,255 ,255 ,50 )))
        p .setPen (QPen (QColor (255 ,255 ,255 ,200 ),1.8 ))
        p .drawEllipse (w -34 ,(h -24 )//2 ,24 ,24 )
        p .setPen (QPen (QColor (255 ,255 ,255 ),2 ))
        ax =w -34 +12 ;ay =h //2 
        p .drawLine (ax -4 ,ay -4 ,ax +2 ,ay );p .drawLine (ax -4 ,ay +4 ,ax +2 ,ay )
        p .end ()


class HeartsWidget (QWidget ):
    """Displays ❤️ / 🤍 lives counter."""

    def __init__ (self ,max_hearts =3 ,parent =None ):
        super ().__init__ (parent )
        self ._max =max_hearts 
        self ._hearts =max_hearts 
        self .setFixedHeight (28 )

    def set_hearts (self ,n :int )->None :
        self ._hearts =max (0 ,min (n ,self ._max ));self .update ()

    def hearts (self )->int :
        return self ._hearts 

    def paintEvent (self ,event ):
        p =QPainter (self );p .setRenderHint (QPainter .Antialiasing )
        p .setFont (QFont ("Segoe UI Emoji",16 ))
        text ="".join ("❤️"if i <self ._hearts else "🤍"for i in range (self ._max ))
        p .drawText (self .rect (),Qt .AlignCenter ,text );p .end ()


class FullScreenEmojiOverlay (QWidget ):
    """
    Full-screen overlay that shows the target emoji + countdown.
    Used by EmojiGameScreen during the memorization phase.
    """

    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        self .setFixedSize (APP_W ,APP_H )
        self .hide ()
        self .setAttribute (Qt .WA_TransparentForMouseEvents )
        self ._emoji ="😊"
        self ._countdown =3 

    def show_emoji (self ,emoji :str ,countdown :int =3 )->None :
        self ._emoji =emoji ;self ._countdown =countdown 
        self .raise_ ();self .show ();self .update ()

    def set_countdown (self ,n :int )->None :
        self ._countdown =n ;self .update ()

    def paintEvent (self ,event ):
        p =QPainter (self );p .setRenderHint (QPainter .Antialiasing )
        p .fillRect (0 ,0 ,APP_W ,APP_H ,QColor (255 ,255 ,255 ,210 ))

        ring =QRadialGradient (APP_W /2 ,APP_H //2 -20 ,140 )
        ring .setColorAt (0 ,QColor (32 ,196 ,185 ,45 ));ring .setColorAt (1 ,QColor (138 ,92 ,210 ,10 ))
        p .setBrush (QBrush (ring ));p .setPen (Qt .NoPen )
        p .drawEllipse (APP_W //2 -130 ,APP_H //2 -150 ,260 ,260 )

        p .setFont (QFont ("Segoe UI Emoji",96 ));p .setPen (QColor (30 ,30 ,30 ))
        p .drawText (QRect (0 ,APP_H //2 -120 ,APP_W ,140 ),Qt .AlignCenter ,self ._emoji )

        p .setFont (QFont ("Arial Rounded MT Bold",18 ,QFont .Weight .Bold ))
        p .setPen (QColor (90 ,45 ,158 ))
        p .drawText (QRect (0 ,APP_H //2 +30 ,APP_W ,36 ),Qt .AlignCenter ,"Look carefully!")

        if self ._countdown >0 :
            p .setFont (QFont ("Arial Rounded MT Bold",28 ,QFont .Weight .Bold ))
            p .setPen (QColor (32 ,196 ,185 ))
            p .drawText (QRect (0 ,APP_H //2 +68 ,APP_W ,40 ),Qt .AlignCenter ,str (self ._countdown ))
        p .end ()







class OnboardingScreen (QWidget ):
    """
    First-run screen: collects child's name and age.
    Emits accepted(name, age) when the child taps "Start Journey".
    DB integration: add_child() is called here before emitting.
    """
    accepted =pyqtSignal (str ,int )

    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        self .setFixedSize (APP_W ,APP_H )
        self ._bg =AnimatedBG (self );self ._bg .lower ()
        self ._age_value =7 
        self ._setup_ui ()


    def _setup_ui (self ):

        layout =QHBoxLayout (self )
        layout .setAlignment (Qt .AlignCenter )
        layout .setContentsMargins (20 ,15 ,20 ,15 )
        layout .setSpacing (15 )



        left_col =QVBoxLayout ()
        left_col .setAlignment (Qt .AlignCenter )

        logo_lbl =QLabel (self )
        logo_lbl .setAlignment (Qt .AlignCenter )
        logo_lbl .setFixedHeight (110 )


        logo_pix =load_pixmap_fit (ASSET_LOGO_FULL ,240 ,100 )
        if logo_pix .isNull ():

            logo_pix =load_pixmap_fit (ASSET_LOGO ,90 ,90 )

        if not logo_pix .isNull ():
            logo_lbl .setPixmap (logo_pix )
            logo_lbl .setStyleSheet ("background: transparent;")
        else :
            logo_lbl .setText ("🌟")
            logo_lbl .setStyleSheet ("font-size: 50px; background: transparent;")
        left_col .addWidget (logo_lbl )

        hello_lbl =QLabel ("Welcome to EmoBridge",self )
        hello_lbl .setAlignment (Qt .AlignCenter )
        hello_lbl .setStyleSheet ("""
            font-family:'Segoe UI','Arial Rounded MT Bold',Arial;
            font-size:16px; font-weight:800; color:#4c1d95;
            background:transparent; margin-bottom:2px;
        """)
        left_col .addWidget (hello_lbl )

        sub_lbl =QLabel ("Set up your profile to begin",self )
        sub_lbl .setAlignment (Qt .AlignCenter )
        sub_lbl .setStyleSheet ("font-size:11px; color:#64748b; background:transparent;")
        left_col .addWidget (sub_lbl )


        right_col =QVBoxLayout ()
        right_col .setAlignment (Qt .AlignCenter )

        card =GlassCard (self ,radius =18 )
        card_lay =QVBoxLayout (card )
        card_lay .setContentsMargins (12 ,12 ,12 ,12 )
        card_lay .setSpacing (8 )


        card_lay .addWidget (self ._field_label ("YOUR NAME",card ))
        self .name_input =QLineEdit (card )
        self .name_input .setPlaceholderText ("Enter your name")
        self .name_input .setFixedHeight (36 )
        self .name_input .setStyleSheet ("""
            QLineEdit { border:2px solid rgba(32,196,185,0.50); border-radius:10px; padding:4px 10px; font-size:13px; font-weight:600; color:#1e293b; background:rgba(255,255,255,0.92); }
            QLineEdit:focus { border:2px solid #8a5cd2; background:rgba(255,255,255,0.98); }
        """)
        card_lay .addWidget (self .name_input )


        divider =QFrame (card )
        divider .setFrameShape (QFrame .HLine )
        divider .setStyleSheet ("background:rgba(138,92,210,0.18); border:none;")
        divider .setFixedHeight (1 )
        card_lay .addWidget (divider )


        card_lay .addWidget (self ._field_label ("YOUR AGE",card ))
        age_row =QHBoxLayout ()
        age_row .setSpacing (8 )
        age_row .setContentsMargins (0 ,0 ,0 ,0 )

        btn_style ="""
            QPushButton { background:rgba(32,196,185,0.15); border:2px solid #20c4b9; border-radius:14px; font-size:18px; font-weight:700; color:#0f766e; }
            QPushButton:pressed { background:rgba(32,196,185,0.35); }
        """

        minus_btn =QPushButton ("−",card )
        minus_btn .setFixedSize (30 ,30 )
        minus_btn .setCursor (Qt .PointingHandCursor )
        minus_btn .setStyleSheet (btn_style )
        minus_btn .clicked .connect (self ._age_down )

        self .age_display =QLabel ("7",card )
        self .age_display .setAlignment (Qt .AlignCenter )
        self .age_display .setFixedSize (50 ,30 )
        self .age_display .setStyleSheet ("""
            font-size:15px; font-weight:800; color:#5a2d9e; background:rgba(255,255,255,0.95); 
            border:2px solid rgba(138,92,210,0.40); border-radius:10px;
        """)

        plus_btn =QPushButton ("+",card )
        plus_btn .setFixedSize (30 ,30 )
        plus_btn .setCursor (Qt .PointingHandCursor )
        plus_btn .setStyleSheet (btn_style )
        plus_btn .clicked .connect (self ._age_up )

        years_lbl =QLabel ("years old",card )
        years_lbl .setStyleSheet ("font-size:11px; color:#64748b; background:transparent;")

        age_row .addWidget (minus_btn )
        age_row .addWidget (self .age_display )
        age_row .addWidget (plus_btn )
        age_row .addWidget (years_lbl )
        age_row .addStretch ()
        card_lay .addLayout (age_row )

        self .error_lbl =QLabel ("",card )
        self .error_lbl .setAlignment (Qt .AlignCenter )
        self .error_lbl .setStyleSheet ("font-size:10px; color:#ef4444; background:transparent;")
        self .error_lbl .hide ()
        card_lay .addWidget (self .error_lbl )

        right_col .addWidget (card )
        right_col .addSpacing (10 )

        ok_btn =QPushButton ("Start Journey →",self )
        ok_btn .setFixedHeight (40 )
        ok_btn .setCursor (Qt .PointingHandCursor )
        ok_btn .setStyleSheet ("""
            QPushButton { background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #20c4b9,stop:1 #7c3aed); color:white; border:none; border-radius:20px; font-size:14px; font-weight:800; font-family:'Segoe UI',Arial; }
            QPushButton:hover { background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #2dd4bf,stop:1 #8b5cf6); }
            QPushButton:pressed { padding-top:2px; }
        """)
        ok_btn .clicked .connect (self ._on_start )
        right_col .addWidget (ok_btn )



        layout .addLayout (left_col ,40 )
        layout .addLayout (right_col ,60 )

    @staticmethod 
    def _field_label (text :str ,parent )->QLabel :
        lbl =QLabel (text ,parent )
        lbl .setStyleSheet ("""
            font-size:11px; font-weight:700; color:#8a5cd2;
            text-transform:uppercase; letter-spacing:1px; background:transparent;
        """)
        return lbl 


    def _age_up (self ):
        if self ._age_value <18 :
            self ._age_value +=1 ;self .age_display .setText (str (self ._age_value ))

    def _age_down (self ):
        if self ._age_value >3 :
            self ._age_value -=1 ;self .age_display .setText (str (self ._age_value ))

    def _on_start (self ):
        """Validate → save to DB → emit accepted signal."""
        name_val =self .name_input .text ().strip ()
        if not name_val :
            self .error_lbl .setText ("Please enter a name!");self .error_lbl .show ();return 

        age_val =self ._age_value 


        try :
            add_child (name_val ,age_val ,"Avatar_Default","Default")
            child_info =search_child (name_val )
            if child_info :
                global CURRENT_CHILD_ID 
                CURRENT_CHILD_ID =child_info [0 ]
        except Exception :
            pass 

        self .error_lbl .hide ()
        self .accepted .emit (name_val ,age_val )



class HomeScreen (QWidget ):
    """
    Main hub screen with Play / Progress / Theme buttons.
    Public API for AI integration:
      set_xp(xp)                  — update XP bar
      set_avatar_image(filename)  — update avatar thumbnail
    """
    go_play =pyqtSignal ()
    go_progress =pyqtSignal ()
    go_theme =pyqtSignal ()

    def __init__ (self ,user_name ="",user_age =7 ,parent =None ):
        super ().__init__ (parent )
        self .user_name =user_name 
        self .user_age =user_age 
        self .xp =0 
        self ._xp_bar_max_w =130 
        self .setFixedSize (APP_W ,APP_H )
        self ._bg =AnimatedBG (self );self ._bg .lower ()
        self ._wave =WaveHeader (self );self ._wave .move (0 ,0 );self ._wave .raise_ ()
        self ._setup_ui ()


    def set_xp (self ,xp :int )->None :
        self .xp =xp 
        self .xp_val_lbl .setText (f"{xp } XP")
        bar_w =min (int ((xp /500 )*self ._xp_bar_max_w ),self ._xp_bar_max_w )
        self .xp_bar .setFixedWidth (max (bar_w ,0 ))

    def set_avatar_image (self ,filename_or_emoji :str )->None :
        pix =load_pixmap_fit (filename_or_emoji ,60 ,60 )
        if not pix .isNull ():
            self .avatar_lbl .setPixmap (pix )
            self .avatar_lbl .setStyleSheet ("border:2px solid #20c4b9; border-radius:14px; background:rgba(255,255,255,0.5);")
        else :
            self .avatar_lbl .setPixmap (QPixmap ())
            self .avatar_lbl .setText (filename_or_emoji )
            self .avatar_lbl .setStyleSheet ("font-size:36px; border:2px solid #20c4b9; border-radius:14px; background:rgba(32,196,185,0.10);")


    def _setup_ui (self ):

        LEFT_W =195 
        RIGHT_W =480 -LEFT_W 
        MARGIN =12 

        root =QHBoxLayout (self )
        root .setContentsMargins (0 ,0 ,0 ,0 )
        root .setSpacing (0 )




        left_panel =QWidget (self )
        left_panel .setFixedSize (LEFT_W ,320 )
        left_panel .setAttribute (Qt .WA_TranslucentBackground )

        left_lay =QVBoxLayout (left_panel )
        left_lay .setContentsMargins (MARGIN ,MARGIN ,6 ,MARGIN )
        left_lay .setSpacing (0 )


        self .logo_lbl =QLabel (left_panel )
        LOGO_W =LEFT_W -MARGIN -6 
        LOGO_H =105 
        self .logo_lbl .setFixedSize (LOGO_W ,LOGO_H )
        self .logo_lbl .setAlignment (Qt .AlignCenter )

        logo_pix =load_pixmap_fit (ASSET_LOGO_FULL ,LOGO_W ,LOGO_H )
        if logo_pix .isNull ():
            logo_pix =load_pixmap_fit (ASSET_LOGO ,LOGO_H ,LOGO_H )

        if not logo_pix .isNull ():
            self .logo_lbl .setPixmap (logo_pix )
            self .logo_lbl .setStyleSheet ("background:transparent; border:none;")
        else :
            self .logo_lbl .setStyleSheet (
            "border:2px dashed #20c4b9; border-radius:8px;"
            "background:rgba(32,196,185,0.10); color:#20c4b9;"
            "font-size:18px; font-weight:900;"
            )
            self .logo_lbl .setText ("EmoBridge")

        left_lay .addWidget (self .logo_lbl )
        left_lay .addSpacing (6 )


        CARD_H =320 -LOGO_H -MARGIN *2 -12 
        profile_card =GlassCard (left_panel ,radius =18 )
        profile_card .setFixedSize (LEFT_W -MARGIN -6 ,CARD_H )

        pc_lay =QVBoxLayout (profile_card )
        pc_lay .setContentsMargins (10 ,10 ,10 ,10 )
        pc_lay .setSpacing (6 )
        pc_lay .setAlignment (Qt .AlignCenter )


        self .avatar_lbl =QLabel (profile_card )
        AV =55 
        self .avatar_lbl .setFixedSize (AV ,AV )
        self .avatar_lbl .setAlignment (Qt .AlignCenter )
        self .avatar_lbl .setStyleSheet (
        f"border:2px dashed #20c4b9; border-radius:{AV //2 }px;"
        "background:rgba(32,196,185,0.12); color:#20c4b9; font-size:9px;"
        )
        self .avatar_lbl .setText ("AVATAR")
        pc_lay .addWidget (self .avatar_lbl ,alignment =Qt .AlignHCenter )


        self .name_lbl =QLabel (profile_card )
        self .name_lbl .setAlignment (Qt .AlignCenter )
        display_name =self .user_name 
        self .name_lbl .setText (display_name )
        self .name_lbl .setStyleSheet (
        "font-family:'Segoe UI','Arial Rounded MT Bold',Arial;"
        "font-size:14px; font-weight:900; color:#1e3a5f; background:transparent;"
        )
        pc_lay .addWidget (self .name_lbl ,alignment =Qt .AlignHCenter )


        xp_label_row =QHBoxLayout ()
        xp_label_row .setSpacing (4 )
        xp_label_row .setAlignment (Qt .AlignCenter )

        star_lbl =QLabel ("⭐",profile_card )
        star_lbl .setStyleSheet ("font-size:12px; background:transparent;")
        xp_label_row .addWidget (star_lbl )

        self .xp_val_lbl =QLabel ("0 XP",profile_card )
        self .xp_val_lbl .setStyleSheet (
        "font-size:12px; font-weight:800; color:#5a2d9e; background:transparent;"
        )
        xp_label_row .addWidget (self .xp_val_lbl )
        pc_lay .addLayout (xp_label_row )


        CARD_INNER_W =LEFT_W -MARGIN -6 -20 
        self ._xp_bar_max_w =CARD_INNER_W 
        xp_bar_bg =QWidget (profile_card )
        xp_bar_bg .setFixedSize (CARD_INNER_W ,8 )
        xp_bar_bg .setStyleSheet ("background:rgba(90,45,158,0.15); border-radius:4px;")

        self .xp_bar =QWidget (xp_bar_bg )
        self .xp_bar .setGeometry (0 ,0 ,0 ,8 )
        self .xp_bar .setStyleSheet (
        "background:qlineargradient(x1:0,y1:0,x2:1,y2:0,"
        "stop:0 #20c4b9, stop:1 #8a5cd2); border-radius:4px;"
        )
        pc_lay .addWidget (xp_bar_bg ,alignment =Qt .AlignHCenter )
        pc_lay .addStretch ()

        left_lay .addWidget (profile_card )
        root .addWidget (left_panel )




        right_panel =QWidget (self )
        right_panel .setAttribute (Qt .WA_TranslucentBackground )
        right_panel .setSizePolicy (QSizePolicy .Expanding ,QSizePolicy .Expanding )

        right_lay =QVBoxLayout (right_panel )

        right_lay .setContentsMargins (10 ,MARGIN ,10 ,MARGIN )
        right_lay .setSpacing (0 )

        right_lay .addStretch ()

        self .games_btn =GradientButton ("Play Games","🎮",[QColor (39 ,193 ,214 ),QColor (26 ,157 ,190 )])
        self .progress_btn =GradientButton ("My Progress","📊",[QColor (106 ,90 ,205 ),QColor (75 ,46 ,131 )])
        self .theme_btn =GradientButton ("Change Theme","🎨",[QColor (168 ,85 ,247 ),QColor (99 ,179 ,237 )])


        BTN_W =260 
        BTN_H =52 
        self .games_btn .setFixedSize (BTN_W ,BTN_H )
        self .progress_btn .setFixedSize (BTN_W ,BTN_H )
        self .theme_btn .setFixedSize (BTN_W ,BTN_H )

        self .games_btn .clicked .connect (self .go_play .emit )
        self .progress_btn .clicked .connect (self .go_progress .emit )
        self .theme_btn .clicked .connect (self .go_theme .emit )

        right_lay .addWidget (self .games_btn ,alignment =Qt .AlignHCenter )
        right_lay .addSpacing (14 )
        right_lay .addWidget (self .progress_btn ,alignment =Qt .AlignHCenter )
        right_lay .addSpacing (14 )
        right_lay .addWidget (self .theme_btn ,alignment =Qt .AlignHCenter )

        right_lay .addStretch ()

        root .addWidget (right_panel )


class GameSelectionScreen (QWidget ):
    """Shows two game cards; emits the appropriate signal on tap."""
    go_emoji_game =pyqtSignal ()
    go_color_game =pyqtSignal ()
    go_back =pyqtSignal ()

    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        self .setFixedSize (APP_W ,APP_H )
        self ._bg =AnimatedBG (self );self ._bg .lower ()
        self ._setup_ui ()

    def _setup_ui (self ):

        layout =QVBoxLayout (self )
        layout .setContentsMargins (20 ,20 ,20 ,20 )
        layout .setSpacing (15 )




        top_bar =QHBoxLayout ()


        self .back_btn =QPushButton ("⬅ Back",self )
        self .back_btn .setFixedSize (80 ,35 )
        self .back_btn .setCursor (Qt .PointingHandCursor )
        self .back_btn .setStyleSheet ("""
            QPushButton {
                background: #f1f5f9; color: #475569; 
                border-radius: 10px; font-weight: bold; font-size: 13px;
                border: 1px solid #cbd5e1;
            }
            QPushButton:hover { background: #e2e8f0; border: 1px solid #94a3b8; }
        """)


        title =QLabel ("Choose a Game",self )
        title .setAlignment (Qt .AlignCenter )
        title .setStyleSheet ("font-family:'Arial Rounded MT Bold',Arial; font-size: 20px; font-weight: 900; color: #4c1d95; background: transparent;")


        dummy_spacer =QLabel (self )
        dummy_spacer .setFixedSize (80 ,35 )
        dummy_spacer .setStyleSheet ("background: transparent;")

        top_bar .addWidget (self .back_btn )
        top_bar .addWidget (title )
        top_bar .addWidget (dummy_spacer )

        layout .addLayout (top_bar )
        layout .addSpacing (10 )




        games_layout =QHBoxLayout ()
        games_layout .setSpacing (30 )
        games_layout .setAlignment (Qt .AlignCenter )


        game_btn_style ="""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 %s, stop:1 %s);
                border-radius: 20px;
                color: white;
                font-family: 'Segoe UI', Arial;
                font-weight: 800;
                font-size: 16px;
                border: 2px solid rgba(255, 255, 255, 0.4);
            }
            QPushButton:hover { 
                border: 2px solid white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 %s, stop:1 %s);
            }
        """


        self .game1_btn =QPushButton ("😄\n\nMatch the Feeling",self )
        self .game1_btn .setFixedSize (180 ,150 )
        self .game1_btn .setCursor (Qt .PointingHandCursor )
        self .game1_btn .setStyleSheet (game_btn_style %("#38bdf8","#2563eb","#7dd3fc","#3b82f6"))


        self .game2_btn =QPushButton ("🎨\n\nColor the Feelings",self )
        self .game2_btn .setFixedSize (180 ,150 )
        self .game2_btn .setCursor (Qt .PointingHandCursor )
        self .game2_btn .setStyleSheet (game_btn_style %("#c084fc","#7e22ce","#d8b4fe","#9333ea"))


        games_layout .addWidget (self .game1_btn )
        games_layout .addWidget (self .game2_btn )

        layout .addLayout (games_layout )
        layout .addStretch ()




        self .back_btn .clicked .connect (self .go_back .emit )
        self .game1_btn .clicked .connect (self .go_emoji_game .emit )
        self .game2_btn .clicked .connect (self .go_color_game .emit )

    @staticmethod 
    def _back_button ()->QPushButton :
        btn =QPushButton ("← Back");btn .setFixedHeight (32 )
        btn .setStyleSheet ("QPushButton { background:rgba(255,255,255,0.7); border:none; border-radius:16px; color:#5a2d9e; font-size:12px; font-weight:700; padding:0 14px; }")
        return btn 

    def _create_game_card (self ,emoji ,title ,desc ,colors ,icon_bg )->QWidget :
        card =QWidget (self );card .setFixedHeight (130 )
        card .setStyleSheet (f"""
            QWidget {{ background:rgba(255,255,255,0.85); border:2px solid rgba(255,255,255,0.9); border-radius:20px; }}
            QWidget:hover {{ background:rgba(255,255,255,0.95); border:2px solid {colors [0 ].name ()}; }}
        """)
        layout =QHBoxLayout (card );layout .setContentsMargins (16 ,14 ,16 ,14 );layout .setSpacing (14 )

        icon_frame =QLabel (card );icon_frame .setFixedSize (68 ,68 );icon_frame .setAlignment (Qt .AlignCenter )
        icon_frame .setText (emoji )
        icon_frame .setStyleSheet (f"""
            font-size:36px;
            background:rgba({icon_bg .red ()},{icon_bg .green ()},{icon_bg .blue ()},0.2);
            border:2px solid rgba({colors [0 ].red ()},{colors [0 ].green ()},{colors [0 ].blue ()},0.4);
            border-radius:34px;
        """)
        layout .addWidget (icon_frame )

        text_col =QVBoxLayout ();text_col .setSpacing (4 )
        title_lbl =QLabel (title ,card )
        title_lbl .setStyleSheet (f"font-family:'Arial Rounded MT Bold',Arial; font-size:15px; font-weight:900; color:{colors [0 ].darker (130 ).name ()}; background:transparent;")
        text_col .addWidget (title_lbl )
        desc_lbl =QLabel (desc ,card );desc_lbl .setWordWrap (True )
        desc_lbl .setStyleSheet ("font-size:11px; color:#6b7280; background:transparent; line-height:1.3;")
        text_col .addWidget (desc_lbl )
        play_lbl =QLabel ("Play →",card )
        play_lbl .setStyleSheet (f"font-size:11px; font-weight:800; color:{colors [0 ].name ()}; background:transparent;")
        text_col .addWidget (play_lbl )
        layout .addLayout (text_col )
        return card 



class EmojiGameScreen (QWidget ):
    """
    "Match the Feeling" game.
    Flow: overlay shows target emoji for 3 s → child picks from 4 choices.
    Signals:
      xp_earned(int)  — earned XP (connect to AppController._add_xp)
      go_back()       — session ended or Back pressed
    Public:
      reset_session() — called before showing this screen
    """
    xp_earned =pyqtSignal (int )
    go_back =pyqtSignal ()

    EMOJIS =["😊","😢","😡","😱","😴","🤩","😂","😎","🥰","😤","🤔","😶"]
    TOTAL_ROUNDS =8 
    CHOICE_STYLE ="""
        QPushButton { font-size:38px; background:rgba(255,255,255,0.82);
            border:3px solid rgba(32,196,185,0.45); border-radius:18px; }
        QPushButton:hover { border-color:#20c4b9; background:rgba(32,196,185,0.18); }
        QPushButton:disabled { opacity:0.55; }
    """

    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        self .setFixedSize (APP_W ,APP_H )
        self ._bg =AnimatedBG (self );self ._bg .lower ()
        self ._current_emoji ="😊"
        self ._score =0 
        self ._round =0 
        self ._hearts =3 
        self ._phase ="show"
        self ._countdown =3 
        self ._setup_ui ()


        self ._overlay =FullScreenEmojiOverlay (self )
        self ._overlay .hide ()

        self ._timer =QTimer (self )
        self ._timer .timeout .connect (self ._tick )

        self ._transition_timer =QTimer (self )
        self ._transition_timer .setSingleShot (True )
        self ._transition_timer .timeout .connect (self ._next_round )


    def reset_session (self )->None :
        """Reset all state and start round 1. Call before showing screen."""
        global GAME_START_TIME ,TOTAL_ATTEMPTS ,SUCCESSFUL_ATTEMPTS ,DISTRACTION_COUNT 
        GAME_START_TIME =datetime .datetime .now ().strftime ("%Y-%m-%d %H:%M:%S")
        TOTAL_ATTEMPTS =0 
        SUCCESSFUL_ATTEMPTS =0 
        DISTRACTION_COUNT =0 

        self ._score =0 ;self ._round =0 ;self ._hearts =3 
        self .hearts_widget .set_hearts (3 )
        self .session_bar .setValue (0 )
        self .score_lbl .setText ("Score: 0  •  +10 XP per win")
        self .feedback_lbl .setText ("")
        self ._timer .stop ();self ._transition_timer .stop ()
        self ._next_round ()


    def hideEvent (self ,event ):
        self ._timer .stop ();self ._transition_timer .stop ()
        super ().hideEvent (event )


    def _setup_ui (self ):
        self ._content =QWidget (self )


        main =QHBoxLayout (self ._content )
        main .setContentsMargins (15 ,15 ,15 ,15 )
        main .setSpacing (20 )




        left_panel =QVBoxLayout ()
        left_panel .setAlignment (Qt .AlignTop )
        left_panel .setSpacing (8 )


        top_row =QHBoxLayout ()
        back_btn =QPushButton ("← Back",self ._content )
        back_btn .setFixedSize (70 ,30 )
        back_btn .setCursor (Qt .PointingHandCursor )
        back_btn .setStyleSheet ("QPushButton { background:rgba(255,255,255,0.75); border:none; border-radius:15px; color:#5a2d9e; font-size:12px; font-weight:700; }")
        back_btn .clicked .connect (self ._on_back_pressed )
        top_row .addWidget (back_btn )
        top_row .addStretch ()

        self .hearts_widget =HeartsWidget (3 ,self ._content )
        top_row .addWidget (self .hearts_widget )
        left_panel .addLayout (top_row )
        left_panel .addSpacing (10 )


        title =QLabel ("Match the Feeling",self ._content )
        title .setAlignment (Qt .AlignCenter )
        title .setStyleSheet ("font-family:'Segoe UI','Arial Rounded MT Bold',Arial; font-size:16px; font-weight:800; color:#5a2d9e; background:transparent;")
        left_panel .addWidget (title )


        self .round_lbl =QLabel ("Round 1 / 8",self ._content )
        self .round_lbl .setAlignment (Qt .AlignCenter )
        self .round_lbl .setStyleSheet ("font-size:12px; color:#64748b; font-weight:600; background:transparent;")
        left_panel .addWidget (self .round_lbl )


        self .session_bar =QProgressBar (self ._content )
        self .session_bar .setRange (0 ,self .TOTAL_ROUNDS )
        self .session_bar .setValue (0 )
        self .session_bar .setFixedHeight (8 )
        self .session_bar .setTextVisible (False )
        self .session_bar .setStyleSheet ("""
            QProgressBar { background:rgba(90,45,158,0.12); border-radius:4px; border:none; }
            QProgressBar::chunk { background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #20c4b9,stop:1 #8a5cd2); border-radius:4px; }
        """)
        left_panel .addWidget (self .session_bar )


        self .score_lbl =QLabel ("Score: 0\n+10 XP per win",self ._content )
        self .score_lbl .setAlignment (Qt .AlignCenter )
        self .score_lbl .setStyleSheet ("font-size:12px; color:#20c4b9; font-weight:700; background:transparent;")
        left_panel .addWidget (self .score_lbl )

        left_panel .addStretch ()


        self .feedback_lbl =QLabel ("",self ._content )
        self .feedback_lbl .setAlignment (Qt .AlignCenter )
        self .feedback_lbl .setWordWrap (True )
        self .feedback_lbl .setStyleSheet ("font-size:15px; font-weight:800; background:transparent;")
        left_panel .addWidget (self .feedback_lbl )
        left_panel .addStretch ()




        right_panel =QVBoxLayout ()
        right_panel .setAlignment (Qt .AlignCenter )
        right_panel .setSpacing (15 )


        hint_card =GlassCard (self ._content ,radius =20 )
        hint_card .setFixedHeight (100 )
        hc_lay =QVBoxLayout (hint_card )
        self .hint_lbl =QLabel ("Watch the emoji…",hint_card )
        self .hint_lbl .setAlignment (Qt .AlignCenter )
        self .hint_lbl .setStyleSheet ("font-size:18px; color:#8a5cd2; font-weight:700; background:transparent;")
        hc_lay .addWidget (self .hint_lbl )
        right_panel .addWidget (hint_card )


        self .choice_widget =QWidget (self ._content )
        self .choice_grid =QGridLayout (self .choice_widget )
        self .choice_grid .setSpacing (10 )
        self .choice_grid .setContentsMargins (0 ,0 ,0 ,0 )

        self .choice_btns =[]
        for i in range (4 ):
            btn =QPushButton ("😊",self .choice_widget )
            btn .setFixedHeight (65 )
            btn .setCursor (Qt .PointingHandCursor )
            btn .setStyleSheet (self .CHOICE_STYLE )
            btn .clicked .connect (lambda _ ,b =btn :self ._on_choice (b ))
            self .choice_btns .append (btn )
            self .choice_grid .addWidget (btn ,i //2 ,i %2 )

        self .choice_widget .hide ()
        right_panel .addWidget (self .choice_widget )


        main .addLayout (left_panel ,40 )
        main .addLayout (right_panel ,60 )


        root =QVBoxLayout (self )
        root .setContentsMargins (0 ,0 ,0 ,0 )
        root .addWidget (self ._content )


    def _next_round (self ):
        if self ._hearts <=0 :
            return 
        self ._round +=1 
        if self ._round >self .TOTAL_ROUNDS :
            self .feedback_lbl .setText ("🎉 Great job! Session complete!")
            self .feedback_lbl .setStyleSheet ("font-size:15px; color:#10b981; font-weight:800; background:transparent;")
            self .choice_widget .hide ()
            _save_game_result (self ._score ,"EmojiGame")
            QTimer .singleShot (2200 ,self ._safe_go_back )
            return 

        self ._countdown =3 ;self ._phase ="show"
        self ._current_emoji =random .choice (self .EMOJIS )
        self .feedback_lbl .setText ("");self ._reset_choice_styles ()
        self ._set_choices_enabled (False );self .choice_widget .hide ()
        self .hint_lbl .setText ("Watch the emoji carefully…")
        self .round_lbl .setText (f"Round {self ._round } / {self .TOTAL_ROUNDS }")
        self .session_bar .setValue (self ._round -1 )

        choices =[self ._current_emoji ]+random .sample (
        [e for e in self .EMOJIS if e !=self ._current_emoji ],3 )
        random .shuffle (choices )
        for btn ,em in zip (self .choice_btns ,choices ):
            btn .setText (em )

        self ._overlay .show_emoji (self ._current_emoji ,self ._countdown )
        self ._overlay .raise_ ()
        self ._timer .start (1000 )

    def _tick (self ):
        if self ._phase !="show":
            return 
        self ._countdown -=1 
        self ._overlay .set_countdown (max (self ._countdown ,0 ))
        if self ._countdown <=0 :
            self ._phase ="choose"
            self ._overlay .hide ()
            self .hint_lbl .setText ("Which one did you see?")
            self .choice_widget .show ()
            self ._set_choices_enabled (True )
            self ._timer .stop ()

    def _on_choice (self ,btn :QPushButton ):
        global TOTAL_ATTEMPTS ,SUCCESSFUL_ATTEMPTS 
        self ._timer .stop ();self ._set_choices_enabled (False )
        TOTAL_ATTEMPTS +=1 

        if btn .text ()==self ._current_emoji :
            SUCCESSFUL_ATTEMPTS +=1 
            self ._score +=10 
            self .score_lbl .setText (f"Score: {self ._score }  •  +10 XP per win")
            self .feedback_lbl .setText ("Correct! +10 XP ⭐")
            self .feedback_lbl .setStyleSheet ("font-size:15px; color:#10b981; font-weight:800; background:transparent;")
            self .xp_earned .emit (10 )
            self .session_bar .setValue (self ._round )
            btn .setStyleSheet ("QPushButton { font-size:38px; background:rgba(16,185,129,0.28); border:3px solid #10b981; border-radius:18px; }")
            self ._transition_timer .start (1400 )
        else :
            self ._hearts -=1 ;self .hearts_widget .set_hearts (self ._hearts )
            self .feedback_lbl .setText ("Not quite — try the next one! 💛")
            self .feedback_lbl .setStyleSheet ("font-size:15px; color:#ef4444; font-weight:800; background:transparent;")
            btn .setStyleSheet ("QPushButton { font-size:38px; background:rgba(239,68,68,0.22); border:3px solid #ef4444; border-radius:18px; }")
            if self ._hearts <=0 :
                self .feedback_lbl .setText ("Out of hearts — good try! 🌈")
                _save_game_result (self ._score ,"EmojiGame")
                QTimer .singleShot (2000 ,self ._safe_go_back )
            else :
                self ._transition_timer .start (1400 )

    def _on_back_pressed (self ):
        self ._timer .stop ();self ._transition_timer .stop ()
        _save_game_result (self ._score ,"EmojiGame")
        self .go_back .emit ()

    def _safe_go_back (self ):
        if self .isVisible ():
            self .go_back .emit ()

    def _reset_choice_styles (self ):
        for btn in self .choice_btns :
            btn .setStyleSheet (self .CHOICE_STYLE )

    def _set_choices_enabled (self ,enabled :bool ):
        for btn in self .choice_btns :
            btn .setEnabled (enabled )



class ColorFeelingsGame (QWidget ):
    """
    "Color the Feelings" game — link emotions to colors.
    Same signal/API contract as EmojiGameScreen.
    """
    xp_earned =pyqtSignal (int )
    go_back =pyqtSignal ()

    FEELINGS =[
    {"emoji":"😊","name":"Happy","color":"#FFD700","color_name":"Yellow"},
    {"emoji":"😢","name":"Sad","color":"#4169E1","color_name":"Blue"},
    {"emoji":"😡","name":"Angry","color":"#DC143C","color_name":"Red"},
    {"emoji":"😱","name":"Scared","color":"#9333EA","color_name":"Purple"},
    {"emoji":"😴","name":"Sleepy","color":"#334155","color_name":"Dark"},
    {"emoji":"🤩","name":"Excited","color":"#FF8C00","color_name":"Orange"},
    {"emoji":"😌","name":"Calm","color":"#2E8B57","color_name":"Green"},
    {"emoji":"🥰","name":"Love","color":"#FF69B4","color_name":"Pink"},
    ]
    ALL_COLORS =["#FFD700","#4169E1","#DC143C","#9333EA","#334155","#FF8C00","#2E8B57","#FF69B4"]
    TOTAL_ROUNDS =8 

    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        self .setFixedSize (APP_W ,APP_H )
        self ._bg =AnimatedBG (self );self ._bg .lower ()
        self ._score =0 ;self ._round =0 ;self ._hearts =3 
        self ._current_feeling =None 
        self ._shuffled_feelings =[]
        self ._setup_ui ()
        self ._transition_timer =QTimer (self )
        self ._transition_timer .setSingleShot (True )
        self ._transition_timer .timeout .connect (self ._next_round )


    def reset_session (self )->None :
        global GAME_START_TIME ,TOTAL_ATTEMPTS ,SUCCESSFUL_ATTEMPTS ,DISTRACTION_COUNT 
        GAME_START_TIME =datetime .datetime .now ().strftime ("%Y-%m-%d %H:%M:%S")
        TOTAL_ATTEMPTS =0 
        SUCCESSFUL_ATTEMPTS =0 
        DISTRACTION_COUNT =0 
        self ._shuffled_feelings =list (self .FEELINGS );random .shuffle (self ._shuffled_feelings )
        self ._round =0 ;self ._score =0 ;self ._hearts =3 
        self .hearts_widget .set_hearts (3 );self .session_bar .setValue (0 )
        self .score_lbl .setText ("Score: 0  •  +10 XP per win")
        self .feedback_lbl .setText ("")
        self ._transition_timer .stop ()
        self ._next_round ()


    def hideEvent (self ,event ):
        self ._transition_timer .stop ();super ().hideEvent (event )


    def _setup_ui (self ):

        main =QHBoxLayout (self )
        main .setContentsMargins (15 ,15 ,15 ,15 )
        main .setSpacing (20 )




        left_panel =QVBoxLayout ()
        left_panel .setAlignment (Qt .AlignTop )
        left_panel .setSpacing (8 )


        top_row =QHBoxLayout ()
        back_btn =QPushButton ("← Back",self )
        back_btn .setFixedSize (70 ,30 )
        back_btn .setCursor (Qt .PointingHandCursor )
        back_btn .setStyleSheet ("QPushButton { background:rgba(255,255,255,0.75); border:none; border-radius:15px; color:#5a2d9e; font-size:12px; font-weight:700; }")
        back_btn .clicked .connect (self ._on_back_pressed )
        top_row .addWidget (back_btn )
        top_row .addStretch ()


        self .hearts_widget =HeartsWidget (3 ,self )
        self .hearts_widget .set_hearts (3 )
        top_row .addWidget (self .hearts_widget )

        left_panel .addLayout (top_row )
        left_panel .addSpacing (10 )


        title =QLabel ("Color the Feelings 🎨",self )
        title .setAlignment (Qt .AlignCenter )
        title .setStyleSheet ("font-family:'Segoe UI','Arial Rounded MT Bold',Arial; font-size:15px; font-weight:800; color:#5a2d9e; background:transparent;")
        left_panel .addWidget (title )


        self .round_lbl =QLabel ("Round 1 / 8",self )
        self .round_lbl .setAlignment (Qt .AlignCenter )
        self .round_lbl .setStyleSheet ("font-size:12px; color:#64748b; font-weight:600; background:transparent;")
        left_panel .addWidget (self .round_lbl )


        self .session_bar =QProgressBar (self )
        self .session_bar .setRange (0 ,self .TOTAL_ROUNDS )
        self .session_bar .setValue (0 )
        self .session_bar .setFixedHeight (8 )
        self .session_bar .setTextVisible (False )
        self .session_bar .setStyleSheet ("""
            QProgressBar { background:rgba(90,45,158,0.12); border-radius:4px; border:none; }
            QProgressBar::chunk { background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #8a5cd2,stop:1 #FF69B4); border-radius:4px; }
        """)
        left_panel .addWidget (self .session_bar )


        self .score_lbl =QLabel ("Score: 0\n+10 XP per win",self )
        self .score_lbl .setAlignment (Qt .AlignCenter )
        self .score_lbl .setStyleSheet ("font-size:12px; color:#8a5cd2; font-weight:700; background:transparent;")
        left_panel .addWidget (self .score_lbl )

        left_panel .addStretch ()


        self .feedback_lbl =QLabel ("",self )
        self .feedback_lbl .setAlignment (Qt .AlignCenter )
        self .feedback_lbl .setWordWrap (True )
        self .feedback_lbl .setStyleSheet ("font-size:15px; font-weight:800; background:transparent;")
        left_panel .addWidget (self .feedback_lbl )
        left_panel .addStretch ()





        right_panel =QVBoxLayout ()
        right_panel .setAlignment (Qt .AlignCenter )
        right_panel .setSpacing (15 )


        emotion_card =GlassCard (self ,radius =22 )
        emotion_card .setFixedHeight (120 )
        ec_lay =QVBoxLayout (emotion_card )
        ec_lay .setSpacing (2 )
        ec_lay .setAlignment (Qt .AlignCenter )

        self .emoji_display =QLabel ("😊",emotion_card )
        self .emoji_display .setAlignment (Qt .AlignCenter )
        self .emoji_display .setStyleSheet ("font-size:45px; background:transparent;")
        ec_lay .addWidget (self .emoji_display )

        self .emotion_name_lbl =QLabel ("Happy",emotion_card )
        self .emotion_name_lbl .setAlignment (Qt .AlignCenter )
        self .emotion_name_lbl .setStyleSheet ("font-family:'Arial Rounded MT Bold',Arial; font-size:16px; font-weight:800; color:#374151; background:transparent;")
        ec_lay .addWidget (self .emotion_name_lbl )

        self .hint_lbl =QLabel ("What color is this feeling?",emotion_card )
        self .hint_lbl .setAlignment (Qt .AlignCenter )
        self .hint_lbl .setStyleSheet ("font-size:11px; color:#8a5cd2; font-weight:600; background:transparent;")
        ec_lay .addWidget (self .hint_lbl )

        right_panel .addWidget (emotion_card )


        self .choice_widget =QWidget (self )
        self .color_grid =QGridLayout (self .choice_widget )
        self .color_grid .setSpacing (12 )
        self .color_grid .setContentsMargins (0 ,0 ,0 ,0 )

        self .color_btns =[]
        for i in range (4 ):
            btn =QPushButton (self .choice_widget )
            btn .setFixedHeight (55 )
            btn .setCursor (Qt .PointingHandCursor )
            btn .clicked .connect (lambda _ ,b =btn :self ._on_color_choice (b ))
            self .color_btns .append (btn )
            self .color_grid .addWidget (btn ,i //2 ,i %2 )

        right_panel .addWidget (self .choice_widget )


        main .addLayout (left_panel ,40 )
        main .addLayout (right_panel ,60 )


    def _next_round (self ):
        if self ._hearts <=0 :
            return 
        self ._round +=1 

        if self ._round >self .TOTAL_ROUNDS :
            self .feedback_lbl .setText ("🎉 Wonderful! You learned all colors!")
            self .feedback_lbl .setStyleSheet ("font-size:15px; color:#10b981; font-weight:800; background:transparent;")
            self .choice_widget .hide ()
            _save_game_result (self ._score ,"ColorGame")


            celeb =WinCelebrationDialog (self ,xp_earned =self ._score )
            celeb .exec_ ()

            QTimer .singleShot (1000 ,self ._safe_go_back )
            return 

        idx =(self ._round -1 )%len (self ._shuffled_feelings )
        self ._current_feeling =self ._shuffled_feelings [idx ]
        self .round_lbl .setText (f"Round {self ._round } / {self .TOTAL_ROUNDS }")
        self .session_bar .setValue (self ._round -1 )
        self .feedback_lbl .setText ("")
        self .emoji_display .setText (self ._current_feeling ["emoji"])
        self .emotion_name_lbl .setText (self ._current_feeling ["name"])
        self .hint_lbl .setText ("What color is this feeling?")

        correct_color =self ._current_feeling ["color"]
        wrong_colors =[c for c in self .ALL_COLORS if c !=correct_color ]
        all_choices =[correct_color ]+random .sample (wrong_colors ,3 )
        random .shuffle (all_choices )

        color_name_map ={f ["color"]:f ["color_name"]for f in self .FEELINGS }
        for btn ,color in zip (self .color_btns ,all_choices ):
            cname =color_name_map .get (color ,"")
            btn .setText (cname );btn .setProperty ("hex_color",color )
            btn .setStyleSheet (self ._color_btn_style (color ));btn .setEnabled (True )
        self .choice_widget .show ()

    def _on_color_choice (self ,btn :QPushButton ):
        global TOTAL_ATTEMPTS ,SUCCESSFUL_ATTEMPTS 
        chosen_color =btn .property ("hex_color")
        correct_color =self ._current_feeling ["color"]
        TOTAL_ATTEMPTS +=1 

        for b in self .color_btns :
            b .setEnabled (False )


        if chosen_color ==correct_color :
            SUCCESSFUL_ATTEMPTS +=1 
            self ._score +=10 
            self .score_lbl .setText (f"Score: {self ._score }  •  +10 XP per win")
            self .feedback_lbl .setText (f"Correct! {self ._current_feeling ['emoji']} = {btn .text ()} ⭐")
            self .feedback_lbl .setStyleSheet ("font-size:14px; color:#10b981; font-weight:800; background:transparent;")
            self .xp_earned .emit (10 );self .session_bar .setValue (self ._round )
            btn .setStyleSheet (f"QPushButton {{ background:{chosen_color }; border:4px solid #10b981; border-radius:16px; color:white; font-size:13px; font-weight:800; }}")
            self ._transition_timer .start (1400 )


        else :
            self ._hearts -=1 
            self .hearts_widget .set_hearts (self ._hearts )

            color_name_map ={f ["color"]:f ["color_name"]for f in self .FEELINGS }
            correct_name =color_name_map .get (correct_color ,"")
            self .feedback_lbl .setText (f"It was {correct_name }! Try again 💛")
            self .feedback_lbl .setStyleSheet ("font-size:14px; color:#ef4444; font-weight:800; background:transparent;")
            btn .setStyleSheet (f"QPushButton {{ background:{chosen_color }; border:4px solid #ef4444; border-radius:16px; color:white; font-size:13px; font-weight:800; }}")

            for b in self .color_btns :
                if b .property ("hex_color")==correct_color :
                    b .setStyleSheet (f"QPushButton {{ background:{correct_color }; border:4px solid #10b981; border-radius:16px; color:white; font-size:13px; font-weight:800; }}")


            if self ._hearts <=0 :
                self .feedback_lbl .setText ("Out of hearts — good try! 🌈")
                _save_game_result (self ._score ,"ColorGame")
                QTimer .singleShot (2000 ,self ._safe_go_back )
            else :
                self ._transition_timer .start (1400 )

    def _on_back_pressed (self ):
        self ._transition_timer .stop ()
        _save_game_result (self ._score ,"ColorGame")
        self .go_back .emit ()

    def _safe_go_back (self ):
        if self .isVisible ():
            self .go_back .emit ()

    @staticmethod 
    def _color_btn_style (hex_color :str )->str :
        return f"""
            QPushButton {{
                background:{hex_color }; border:3px solid rgba(255,255,255,0.7);
                border-radius:16px; color:white; font-size:13px; font-weight:800;
            }}
            QPushButton:hover {{ border:3px solid rgba(255,255,255,1.0); }}
        """



class LevelUpDialog (QDialog ):
    def __init__ (self ,parent ,level_name ,img_pixmap ):
        super ().__init__ (parent )
        self .setWindowFlags (Qt .FramelessWindowHint |Qt .Dialog )
        self .setAttribute (Qt .WA_TranslucentBackground )
        self .setFixedSize (280 ,320 )

        layout =QVBoxLayout (self )

        card =GlassCard (self ,radius =20 )
        card_lay =QVBoxLayout (card )
        card_lay .setAlignment (Qt .AlignCenter )
        card_lay .setSpacing (15 )

        title =QLabel ("🎉 Level Up! 🎉",card )
        title .setStyleSheet ("font-size:22px; font-weight:900; color:#5a2d9e; background:transparent;")
        title .setAlignment (Qt .AlignCenter )
        card_lay .addWidget (title )

        img_lbl =QLabel (card )
        img_lbl .setAlignment (Qt .AlignCenter )
        if not img_pixmap .isNull ():
            img_lbl .setPixmap (img_pixmap .scaled (100 ,100 ,Qt .KeepAspectRatio ,Qt .SmoothTransformation ))
        card_lay .addWidget (img_lbl )

        msg =QLabel (f"You reached\n{level_name }!",card )
        msg .setAlignment (Qt .AlignCenter )
        msg .setStyleSheet ("font-size:18px; font-weight:bold; color:#374151; background:transparent;")
        card_lay .addWidget (msg )

        btn =QPushButton ("Awesome!",card )
        btn .setFixedHeight (45 )
        btn .setCursor (Qt .PointingHandCursor )
        btn .setStyleSheet ("""
            QPushButton { background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #20c4b9,stop:1 #8a5cd2);
                color:white; border:none; border-radius:20px; font-size:16px; font-weight:bold; }
            QPushButton:hover { opacity:0.9; }
        """)
        btn .clicked .connect (self .accept )
        card_lay .addWidget (btn )

        layout .addWidget (card )
class ProgressScreen (QWidget ):
    """
    Shows overall XP bar and 4 badge levels.
    Public API: update_xp(xp) — call whenever XP changes.
    """
    go_back =pyqtSignal ()

    LEVELS =[
    ("🌱","Happy Friend",0 ,"You're just getting started!"),
    ("⭐","Cool Connector",100 ,"Building strong connections!"),
    ("🏆","Awesome Achiever",250 ,"Great things ahead!"),
    ("👑","Bridge Master",400 ,"You've mastered emotions!"),
    ]

    def __init__ (self ,xp =0 ,parent =None ):
        super ().__init__ (parent )
        self .xp =xp ;self .setFixedSize (APP_W ,APP_H )
        self ._bg =AnimatedBG (self );self ._bg .lower ()
        self ._setup_ui ()

    def update_xp (self ,xp :int )->None :
        self .xp =xp 
        self .xp_bar_fill .setValue (min (xp ,500 ))
        self .xp_label .setText (f"{xp } / 500 XP")
        self ._refresh_badges ()

    def _setup_ui (self ):
        main_layout =QVBoxLayout (self )
        main_layout .setContentsMargins (12 ,12 ,12 ,12 )
        main_layout .setSpacing (10 )


        top_row =QHBoxLayout ()
        top_row .setContentsMargins (0 ,0 ,0 ,0 )
        top_row .setSpacing (10 )

        self .back_btn =QPushButton ("←",self )
        self .back_btn .setFixedSize (32 ,32 )
        self .back_btn .setCursor (Qt .PointingHandCursor )
        self .back_btn .setStyleSheet ("""
            QPushButton { background:rgba(255,255,255,0.7); border:none; border-radius:16px; color:#5a2d9e; font-size:16px; font-weight:bold; }
            QPushButton:hover { background:rgba(255,255,255,0.9); }
        """)
        if hasattr (self ,'go_back'):self .back_btn .clicked .connect (self .go_back .emit )
        top_row .addWidget (self .back_btn )

        title =QLabel ("Progress",self )
        title .setStyleSheet ("font-family:'Segoe UI',Arial; font-size:20px; font-weight:900; color:#5a2d9e; background:transparent;")
        top_row .addWidget (title )
        top_row .addStretch ()
        main_layout .addLayout (top_row )


        content_lay =QHBoxLayout ()
        content_lay .setContentsMargins (0 ,0 ,0 ,0 )
        content_lay .setSpacing (15 )


        left_panel =QVBoxLayout ()
        left_panel .setContentsMargins (0 ,0 ,0 ,0 )

        scroll =QScrollArea (self )
        scroll .setWidgetResizable (True )

        scroll .setHorizontalScrollBarPolicy (Qt .ScrollBarAlwaysOff )
        scroll .setVerticalScrollBarPolicy (Qt .ScrollBarAsNeeded )
        scroll .setStyleSheet ("QScrollArea { border:none; background:transparent; }")

        scroll_content =QWidget ()
        scroll_content .setStyleSheet ("background:transparent;")
        scroll_lay =QVBoxLayout (scroll_content )
        scroll_lay .setContentsMargins (0 ,0 ,0 ,0 )
        scroll_lay .setSpacing (15 )

        self .badge_cards =[]

        self .LEVELS =[
        ("🌟","Starter",0 ,"Just beginning"),
        ("🚀","Explorer",500 ,"Reached 500 XP"),
        ("🦸","Hero",1500 ,"Reached 1500 XP"),
        ("👑","Master",3000 ,"Reached 3000 XP"),
        ]

        for i ,(emoji ,name ,req ,desc )in enumerate (self .LEVELS ):
            row_card =GlassCard (scroll_content ,radius =20 )
            row_card .setFixedHeight (110 )


            opacity_effect =QGraphicsOpacityEffect (row_card )
            row_card .setGraphicsEffect (opacity_effect )

            row_lay =QHBoxLayout (row_card )
            row_lay .setContentsMargins (12 ,10 ,15 ,10 )
            row_lay .setSpacing (20 )

            img_lbl =QLabel (row_card )
            img_lbl .setFixedSize (85 ,85 )
            img_lbl .setAlignment (Qt .AlignCenter )
            img_lbl .setStyleSheet ("border-radius:20px; background:rgba(255,255,255,0.5); border:3px solid rgba(255,255,255,0.8);")

            level_pix =None 
            try :
                if 'ASSET_LEVELS'in globals ()and i <len (ASSET_LEVELS ):
                    level_pix =load_pixmap_fit (ASSET_LEVELS [i ],75 ,75 )
                    img_lbl .setPixmap (level_pix )
                else :
                    img_lbl .setText (emoji )
                    img_lbl .setStyleSheet ("font-size:45px; background:transparent;")
            except :
                img_lbl .setText (emoji )
                img_lbl .setStyleSheet ("font-size:45px; background:transparent;")

            row_lay .addWidget (img_lbl )

            info_col =QVBoxLayout ()
            info_col .setAlignment (Qt .AlignVCenter )

            nm_lbl =QLabel (name ,row_card )
            nm_lbl .setStyleSheet ("font-size:18px; font-weight:900; color:#374151; background:transparent;")

            req_lbl =QLabel (f"{req } XP — {desc }",row_card )
            req_lbl .setStyleSheet ("font-size:13px; font-weight:700; color:#6b7280; background:transparent;")

            info_col .addWidget (nm_lbl )
            info_col .addWidget (req_lbl )
            row_lay .addLayout (info_col )
            row_lay .addStretch ()

            scroll_lay .addWidget (row_card )
            self .badge_cards .append ((row_card ,req ,img_lbl ,opacity_effect ,name ,level_pix ))

        scroll_lay .addStretch ()
        scroll .setWidget (scroll_content )
        left_panel .addWidget (scroll )

        content_lay .addLayout (left_panel ,65 )


        right_panel =QVBoxLayout ()
        right_panel .setAlignment (Qt .AlignTop )

        xp_card =GlassCard (self ,radius =20 )
        xp_card .setFixedHeight (140 )
        xp_lay =QVBoxLayout (xp_card )
        xp_lay .setContentsMargins (15 ,20 ,15 ,20 )
        xp_lay .setAlignment (Qt .AlignCenter )

        xp_title =QLabel ("⭐ Total XP",xp_card )
        xp_title .setAlignment (Qt .AlignCenter )
        xp_title .setStyleSheet ("font-size:15px; font-weight:900; color:#374151; background:transparent;")
        xp_lay .addWidget (xp_title )

        current_xp =getattr (self ,'xp',0 )
        max_xp_val =self .LEVELS [-1 ][2 ]if self .LEVELS else 500 

        self .xp_label =QLabel (f"{current_xp } / {max_xp_val }",xp_card )
        self .xp_label .setAlignment (Qt .AlignCenter )
        self .xp_label .setStyleSheet ("font-size:24px; font-weight:900; color:#5a2d9e; background:transparent;")
        xp_lay .addWidget (self .xp_label )

        self .xp_bar_fill =QProgressBar (xp_card )
        self .xp_bar_fill .setRange (0 ,max_xp_val )
        self .xp_bar_fill .setValue (current_xp )
        self .xp_bar_fill .setFixedHeight (18 )
        self .xp_bar_fill .setTextVisible (False )
        self .xp_bar_fill .setStyleSheet ("""
            QProgressBar { background:rgba(90,45,158,0.15); border-radius:9px; border:none; }
            QProgressBar::chunk { background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #20c4b9,stop:1 #8a5cd2); border-radius:9px; }
        """)
        xp_lay .addWidget (self .xp_bar_fill )

        right_panel .addWidget (xp_card )
        right_panel .addStretch ()
        content_lay .addLayout (right_panel ,35 )

        main_layout .addLayout (content_lay )

        self .last_unlocked_level =None 
        if hasattr (self ,'_refresh_badges'):
            self ._refresh_badges (initial_load =True )

    def _refresh_badges (self ,initial_load =False ):
        current_xp =getattr (self ,'xp',0 )
        highest_new_level =None 
        highest_new_img =None 

        for (card ,req ,img_lbl ,opacity_effect ,name ,pixmap )in getattr (self ,'badge_cards',[]):
            if current_xp >=req :
                opacity_effect .setOpacity (1.0 )
                highest_new_level =name 
                highest_new_img =pixmap 
            else :
                opacity_effect .setOpacity (0.4 )

        if not initial_load and highest_new_level and highest_new_level !=getattr (self ,'last_unlocked_level',None ):
            self .last_unlocked_level =highest_new_level 
            dialog =LevelUpDialog (self ,highest_new_level ,highest_new_img )
            dialog .exec_ ()
        elif initial_load :
            self .last_unlocked_level =highest_new_level 



class ThemeScreen (QWidget ):
    """
    Avatar picker + background theme picker.
    Background themes auto-detected from assets/background*.png.
    لإضافة ثيم جديد: ضع صورة باسم background2.png, background3.png … في مجلد assets/
    Signals:
      go_back()                    — navigate away
      avatar_changed(asset_name)   — new avatar selected
      theme_bg_changed(filename)   — new background selected
    """
    go_back =pyqtSignal ()
    avatar_changed =pyqtSignal (str )
    theme_bg_changed =pyqtSignal (str )

    FALLBACK_EMOJIS =["🤖","🦊","🐬","🦋","🌟","🦄","🐸","🚀"]

    def __init__ (self ,parent =None ):
        super ().__init__ (parent )
        self .setFixedSize (APP_W ,APP_H )
        self ._bg =AnimatedBG (self );self ._bg .lower ()
        self ._selected =0 
        self ._selected_asset =ASSET_AVATARS [0 ]
        self ._selected_bg ="background.png"
        self ._setup_ui ()

    def _setup_ui (self ):

        main =QVBoxLayout (self )
        main .setContentsMargins (10 ,8 ,10 ,8 )
        main .setSpacing (4 )




        top_row =QHBoxLayout ()
        top_row .setContentsMargins (0 ,0 ,0 ,0 )
        top_row .setSpacing (10 )


        back_btn =QPushButton ("←",self )
        back_btn .setFixedSize (30 ,30 )
        back_btn .setCursor (Qt .PointingHandCursor )
        back_btn .setStyleSheet ("""
            QPushButton { 
                background:rgba(255,255,255,0.7); border:none; border-radius:15px; 
                color:#5a2d9e; font-size:16px; font-weight:bold; padding:0;
            }
            QPushButton:hover { background:rgba(255,255,255,0.9); }
        """)
        back_btn .clicked .connect (self .go_back .emit )
        top_row .addWidget (back_btn )


        title =QLabel ("Avatars",self )
        title .setStyleSheet ("font-family:'Segoe UI',Arial; font-size:15px; font-weight:800; color:#5a2d9e; background:transparent;")
        top_row .addWidget (title )
        top_row .addStretch ()

        main .addLayout (top_row )





        av_widget =QWidget (self )
        av_grid =QGridLayout (av_widget )
        av_grid .setContentsMargins (0 ,0 ,0 ,0 )
        av_grid .setSpacing (4 )

        self .av_btns =[]
        self .av_icons =[]

        for i ,asset_name in enumerate (ASSET_AVATARS ):
            name =AVATAR_NAMES [i ]if i <len (AVATAR_NAMES )else f"Avatar {i +1 }"
            emoji =self .FALLBACK_EMOJIS [i ]if hasattr (self ,'FALLBACK_EMOJIS')and i <len (self .FALLBACK_EMOJIS )else "🙂"

            btn =QPushButton (self )
            btn .setFixedSize (62 ,70 )
            btn .setCursor (Qt .PointingHandCursor )

            btn_lay =QVBoxLayout (btn )
            btn_lay .setContentsMargins (2 ,2 ,2 ,2 )
            btn_lay .setSpacing (1 )

            icon =QLabel (btn )
            icon .setAlignment (Qt .AlignCenter )
            icon .setFixedHeight (42 )

            pix =load_pixmap_fit (asset_name ,40 ,40 )
            if not pix .isNull ():
                icon .setPixmap (pix )
                icon .setStyleSheet ("background:transparent;")
            else :
                icon .setText (emoji )
                icon .setStyleSheet ("font-size:24px; background:transparent;")

            nm =QLabel (name ,btn )
            nm .setAlignment (Qt .AlignCenter )
            nm .setStyleSheet ("font-size:8px; color:#374151; background:transparent; font-weight:600;")

            btn_lay .addWidget (icon )
            btn_lay .addWidget (nm )


            btn .setStyleSheet ("""
                QPushButton { background:rgba(255,255,255,0.78); border:2px solid rgba(32,196,185,0.35); border-radius:14px; }
                QPushButton:hover { border-color:#20c4b9; background:rgba(255,255,255,0.9); }
            """)
            btn .clicked .connect (lambda _ ,idx =i ,asset =asset_name :self ._select (idx ,asset ))

            av_grid .addWidget (btn ,i //4 ,i %4 )
            self .av_btns .append (btn )
            self .av_icons .append (icon )

        main .addWidget (av_widget )







        bg_title =QLabel ("Themes",self )
        bg_title .setStyleSheet ("font-family:'Segoe UI',Arial; font-size:13px; font-weight:700; color:#5a2d9e; background:transparent; margin-top:2px;")
        main .addWidget (bg_title )


        bg_scroll =QScrollArea (self )
        bg_scroll .setFixedHeight (50 )
        bg_scroll .setWidgetResizable (True )
        bg_scroll .setStyleSheet ("QScrollArea { border:none; background:transparent; }")

        bg_widget =QWidget ()
        bg_widget .setStyleSheet ("background:transparent;")
        bg_layout =QHBoxLayout (bg_widget )
        bg_layout .setContentsMargins (2 ,2 ,2 ,2 )
        bg_layout .setSpacing (8 )

        bg_scroll .setWidget (bg_widget )
        main .addWidget (bg_scroll )

        self .bg_btns :list [tuple [QPushButton ,str ]]=[]
        for i ,bg_file in enumerate (get_background_themes ()):
            num_part ="".join (c for c in bg_file if c .isdigit ())
            theme_num =num_part if num_part else str (i +1 )


            btn =QPushButton (f"Theme {theme_num }",bg_widget )
            btn .setFixedSize (85 ,34 )
            btn .setCursor (Qt .PointingHandCursor )

            btn .setStyleSheet ("""
                QPushButton { 
                    background:rgba(255,255,255,0.85); border:1px solid #cbd5e1; border-radius:8px; 
                    font-size:11px; font-weight:bold; color:#334155;
                }
                QPushButton:hover { border:1px solid #8a5cd2; background:white; }
            """)
            btn .clicked .connect (lambda _ ,f =bg_file :self ._select_bg (f ))
            bg_layout .addWidget (btn )
            self .bg_btns .append ((btn ,bg_file ))




        self .confirm_btn =QPushButton ("Save Profile Theme",self )
        self .confirm_btn .setFixedHeight (40 )
        self .confirm_btn .setCursor (Qt .PointingHandCursor )
        self .confirm_btn .setStyleSheet ("""
            QPushButton { 
                background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #20c4b9,stop:1 #8a5cd2);
                color:white; border:none; border-radius:20px; font-size:14px; font-weight:800; 
                margin-top:2px;
            }
            QPushButton:hover { opacity:0.9; }
            QPushButton:pressed { padding-top:2px; }
        """)
        self .confirm_btn .clicked .connect (self ._confirm )
        main .addWidget (self .confirm_btn )




        if ASSET_AVATARS :
            self ._select (0 ,ASSET_AVATARS [0 ])
        self ._select_bg ("background.png")

    def _select (self ,idx :int ,asset_name :str )->None :
        self ._selected =idx ;self ._selected_asset =asset_name 
        for i ,btn in enumerate (self .av_btns ):
            if i ==idx :
                btn .setStyleSheet ("QPushButton { background:rgba(32,196,185,0.22); border:3px solid #20c4b9; border-radius:16px; }")
            else :
                btn .setStyleSheet ("QPushButton { background:rgba(255,255,255,0.78); border:2.5px solid rgba(32,196,185,0.35); border-radius:16px; } QPushButton:hover { border-color:#20c4b9; }")

    def _select_bg (self ,filename :str )->None :
        self ._selected_bg =filename ;self ._update_bg_btn_styles ()

    def _update_bg_btn_styles (self ):
        sel ="QPushButton { background:rgba(32,196,185,0.25); border:3px solid #20c4b9; border-radius:12px; font-weight:800; color:#0f766e; font-size:11px; }"
        unsel ="QPushButton { background:rgba(255,255,255,0.8); border:2px solid rgba(32,196,185,0.35); border-radius:12px; font-weight:700; color:#374151; font-size:11px; }"
        for btn ,bg_file in self .bg_btns :
            btn .setStyleSheet (sel if bg_file ==self ._selected_bg else unsel )

    def _confirm (self ):
        self .avatar_changed .emit (self ._selected_asset )
        self .theme_bg_changed .emit (self ._selected_bg )
        self .go_back .emit ()
        # تشغيل خيط الـ AI مالت عبد الرحمن تلقائياً فور تأكيد بدء الجلسة
        from main import EmotionAIThread
        self.ai_thread = EmotionAIThread()
        self.ai_thread.emotion_detected.connect(lambda em, conf: print(f"Live AI: {em} ({conf:.2f})"))
        self.ai_thread.session_finished.connect(self.save_game_session_data)
        self.ai_thread.start()
        print("📷 [AI Thread] Camera started and monitoring emotion...")






class EmoBridgeApp (QMainWindow ):
    """
    Root window and navigation controller.
    Stack indices after onboarding:
        0 — HomeScreen
        1 — GameSelectionScreen
        2 — EmojiGameScreen
        3 — ColorFeelingsGame
        4 — ProgressScreen
        5 — ThemeScreen
        6 — FinalReportScreen
    """

    def __init__ (self ):
        super ().__init__ ()
        self .setFixedSize (APP_W ,APP_H )
        self .setWindowTitle ("EmoBridge")
        self .setWindowFlags (Qt .FramelessWindowHint )

        self ._xp =0 
        self ._user_name =""
        self ._user_age =7 
        self .home :HomeScreen |None =None 

        self .final_emotion ="normal"
        self .final_engagement ="0%"
        self .final_notes ="analysis in progress..."

        self .stack =QStackedWidget (self )
        self .stack .setFixedSize (APP_W ,APP_H )
        self .setCentralWidget (self .stack )

        self ._build_screens ()


    def _build_screens (self ):

        self .onboarding =OnboardingScreen ()
        self .onboarding .accepted .connect (self ._on_onboarding_done )
        self .stack .addWidget (self .onboarding )
        self .stack .setCurrentIndex (0 )


        self .game_select =GameSelectionScreen ()
        self .emoji_game =EmojiGameScreen ()
        self .color_game =ColorFeelingsGame ()
        self .progress_scr =ProgressScreen (0 )
        self .theme_scr =ThemeScreen ()


        self .emoji_game .xp_earned .connect (self ._add_xp )
        self .color_game .xp_earned .connect (self ._add_xp )


        self .theme_scr .theme_bg_changed .connect (self ._on_theme_bg_changed )
        self .theme_scr .avatar_changed .connect (self ._on_avatar_changed )
        self .final_report_scr =QWidget ()
        report_layout =QVBoxLayout (self .final_report_scr )
        report_layout .setContentsMargins (15 ,15 ,15 ,15 )


        report_card =GlassCard ()
        card_layout =QVBoxLayout (report_card )


        self .report_title =QLabel ("🎉 تقرير الجلسة 🎉")
        self .report_title .setStyleSheet ("font-size: 20px; font-weight: bold; color: white; padding-bottom: 10px;")

        self .final_emotion_lbl =QLabel ("المشاعر المسيطرة: --")
        self .final_emotion_lbl .setStyleSheet ("font-size: 14px; color: #E0E0E0;")

        self .final_engagement_lbl =QLabel ("نسبة التفاعل: --")
        self .final_engagement_lbl .setStyleSheet ("font-size: 14px; color: #E0E0E0;")

        self .final_notes_lbl =QLabel ("التحليل السلوكي:\nجاري بـدء الجلسة...")
        self .final_notes_lbl .setWordWrap (True )
        self .final_notes_lbl .setStyleSheet ("font-size: 13px; color: #B0B0B0; padding-top: 5px;")


        self .back_to_main_btn =GradientButton ("الرئيسية","#4CAF50","#2E7D32")
        self .back_to_main_btn .setFixedSize (140 ,35 )

        # السطر المعدل لإنهاء الجلسة، الحفظ، ثم العودة للشاشة الرئيسية
        self.back_to_main_btn.clicked.connect(self.end_and_save_session)

        card_layout .addWidget (self .report_title ,alignment =Qt .AlignCenter )
        card_layout .addWidget (self .final_emotion_lbl )
        card_layout .addWidget (self .final_engagement_lbl )
        card_layout .addWidget (self .final_notes_lbl )
        card_layout .addSpacing (15 )
        card_layout .addWidget (self .back_to_main_btn ,alignment =Qt .AlignCenter )


        report_layout .addWidget (report_card )


        self .stack .addWidget (self .final_report_scr )


    def end_and_save_session(self):
        # 1. إيقاف خيط الكاميرا مالت عبد الرحمن (إذا كان مشتغل)
        if hasattr(self, 'ai_thread') and self.ai_thread and self.ai_thread.isRunning():
            self.ai_thread.stop()
            print("📷 [AI Thread] Camera stopped successfully.")
            
        # 2. تحويل الشاشة والعودة للرئيسية (كود حيدر الأصلي)
        self.stack.setCurrentIndex(0)


    def _rebuild_stack_post_onboarding (self ):
        """
        After onboarding is done: rebuild stack with correct indices.
        Called once from _on_onboarding_done.
        """
        while self .stack .count ()>0 :
            self .stack .removeWidget (self .stack .widget (0 ))

        self .stack .addWidget (self .home )
        self .stack .addWidget (self .game_select )
        self .stack .addWidget (self .emoji_game )
        self .stack .addWidget (self .color_game )
        self .stack .addWidget (self .progress_scr )
        self .stack .addWidget (self .theme_scr )


        self .home .go_play .connect (lambda :self .stack .setCurrentIndex (1 ))
        self .home .go_progress .connect (lambda :self .stack .setCurrentIndex (4 ))
        self .home .go_theme .connect (lambda :self .stack .setCurrentIndex (5 ))


        self ._reconnect (self .game_select .go_back ,lambda :self .stack .setCurrentIndex (0 ))
        self ._reconnect (self .game_select .go_emoji_game ,self ._start_emoji_game )
        self ._reconnect (self .game_select .go_color_game ,self ._start_color_game )


        self ._reconnect (self .emoji_game .go_back ,lambda :self .stack .setCurrentIndex (1 ))
        self ._reconnect (self .color_game .go_back ,lambda :self .stack .setCurrentIndex (1 ))


        self ._reconnect (self .progress_scr .go_back ,lambda :self .stack .setCurrentIndex (0 ))
        self ._reconnect (self .theme_scr .go_back ,lambda :self .stack .setCurrentIndex (0 ))

        self .stack .setCurrentIndex (0 )

    @staticmethod 
    def _reconnect (signal ,slot ):
        """Safely disconnect all previous connections then connect slot."""
        try :
            signal .disconnect ()
        except Exception :
            pass 
        signal .connect (slot )


    def _on_onboarding_done (self ,name :str ,age :int ):
        self ._user_name =name ;self ._user_age =age 
        self .home =HomeScreen (user_name =name ,user_age =age )
        self ._rebuild_stack_post_onboarding ()

    def _start_emoji_game (self ):
        self .emoji_game .reset_session ()
        self .stack .setCurrentIndex (2 )

    def _start_color_game (self ):
        self .color_game .reset_session ()
        self .stack .setCurrentIndex (3 )

    def _add_xp (self ,amount :int ):
        self ._xp +=amount 
        if self .home :
            self .home .set_xp (self ._xp )
        self .progress_scr .update_xp (self ._xp )

    def _on_avatar_changed (self ,asset_name :str ):
        if self .home :
            self .home .set_avatar_image (asset_name )

    def _on_theme_bg_changed (self ,bg_filename :str ):
        """Propagate background theme to all screens."""
        screens =[
        self .onboarding ,self .home ,self .game_select ,
        self .emoji_game ,self .color_game ,self .progress_scr ,self .theme_scr 
        ]
        for screen in screens :
            if screen and hasattr (screen ,'_bg')and screen ._bg is not None :
                screen ._bg .set_background_image (bg_filename )


    def mousePressEvent (self ,e ):
        if e .button ()==Qt .LeftButton :
            self ._drag_pos =e .globalPos ()-self .frameGeometry ().topLeft ()

    def mouseMoveEvent (self ,e ):
        if e .buttons ()==Qt .LeftButton and hasattr (self ,'_drag_pos'):
            self .move (e .globalPos ()-self ._drag_pos )
    def show_final_analysis (self ,emotion :str ,engagement :str ,notes :str ):
        """
        AI Hook: يستدعيها عبد الرحمن لتمرير النتائج النهائية للواجهة
        """
        self .final_emotion =emotion 
        self .final_engagement =engagement 
        self .final_notes =notes 


        self .final_emotion_lbl .setText (f"المشاعر المسيطرة: {emotion }")
        self .final_engagement_lbl .setText (f"نسبة التفاعل: {engagement }")
        self .final_notes_lbl .setText (f"التحليل السلوكي:\n{notes }")


        self .stack .setCurrentIndex (6 )





def main ():
    app =QApplication (sys .argv )
    app .setStyle ("Fusion")
    win =EmoBridgeApp ()
    win .show ()
    sys .exit (app .exec_ ())


if __name__ =="__main__":
    main ()
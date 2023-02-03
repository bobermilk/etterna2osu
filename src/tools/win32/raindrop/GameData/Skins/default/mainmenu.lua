skin_require "Global/FadeInScreen"
game_require "AnimationFunctions"

Preload = {
	"MainMenu/play.png",
	"MainMenu/quit.png"
}

IntroDuration = 0.5
ExitDuration = 1.5

function UpdateIntro(p, delta)
	local S = elastic(p)
  
  -- At 1/3rd of the screen, please.
	targBadge.Y = ScreenHeight * 3/7 * (S) - targBadge.Height
	targLogo.Y = targBadge.Y
	Update(delta)
	BGAOut(p*p)
end

function OnRunningBegin()
	ScreenFade.Out()
end

function OnRestore()
	ScreenFade.Out()
end

function OnIntroBegin()
	Engine:SetUILayer(31)
end

function OnExitBegin()
end

function UpdateExit(p, delta)
	local ease = p*p
	UpdateIntro(1-p, delta)
	FadeInA1(ease)
	BGAIn(ease)
end

function KeyEvent(k, c, mouse)
	if c == 1 then 
		Global:StartScreen("songselect")
	end
end

function Init()
  elastic = Ease.ElasticSquare(1.5)
	ScreenFade:Init()
	Time = 0
		
	targLogo = Engine:CreateObject() 
	targLogo.Texture = "MainMenu/FRONTs.png"
	targLogo.X = ScreenWidth / 2
	targLogo.Y = ScreenHeight / 4
	targLogo.Centered = 1
	targLogo.Alpha = 1
	targLogo.Layer = 31

	targBadge = Engine:CreateObject()
	targBadge.Texture = "MainMenu/BACKs.png"
	targBadge.X = ScreenWidth / 2
	targBadge.Y = ScreenHeight / 4
	targBadge.Centered = 1
	targBadge.Layer = 31
	
	font = Fonts.TruetypeFont(GetSkinFile("font.ttf"))

	s = "press any key..."
	title = StringObject2D()
	title.Font = font
	title.Y = ScreenHeight * 3 / 4
	title.Text = s
	title.X = ScreenWidth / 2 - title.TextSize / 2
	title.Z = 31
	title.FontSize = 36
	Engine:AddTarget(title)

	-- Rocket UI not initialized yet...
end

function Cleanup()
end

badgeRotSpeed = 1080

function Update(Delta)
	Time = Time + Delta

	title.KernScale = 2 + 0.5 * sin(Time)

	local sc = sin(Time) * 0.2 + 1.2

	title.ScaleX = sc
	title.ScaleY = sc
	title.X = ScreenWidth / 2 - title.TextSize * sc / 2
	badgeRotSpeed = math.max(badgeRotSpeed - Delta * 240, 120)
	targBadge.Rotation = targBadge.Rotation - badgeRotSpeed * Delta
	BackgroundAnimation:Update(Delta)
end

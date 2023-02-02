game_require "librd"
skin_require "Loading/phrases"
game_require "AnimationFunctions"

IntroDuration = 0.35
ExitDuration = 0.35
Acceleration = 0
badgeEase = Ease.ElasticSquare(1.5)


function UpdateIntro(frac, delta)
	targBadge:SetScale(badgeEase(frac))
	targBadge.Rotation = 360 * frac 

	frac =  1 - math.pow(1 - frac, 2)

	if BG then
		BG.Alpha = frac
	end

	BgStuff.ScaleY = frac

	Phrases.Fade(frac)
	Update(delta)
end

function UpdateExit(frac, delta)
	UpdateIntro(1-frac, delta)
end

function Init()
	
	targBadge = Engine:CreateObject()
	
	targBadge.Texture = "Loading/loadingbadge.png"
	targBadge.Centered = 1
	targBadge.Width = 64
	targBadge.Height = 64
	
	wb = targBadge.Width

	targBadge.X = 48
	targBadge.Y = ScreenHeight / 2 - 48
	targBadge.Layer = 16


	BgStuff = Transformation()

	targBackground = Engine:CreateObject()
	targBackground.Texture = "Global/white.png"
	with(targBackground, {
		Red = 0.03,
		Blue = 0.03,
		Green = 0.03,
		Alpha = 0.65,
		Height = ScreenHeight / 3,
		Width = ScreenWidth,
		Layer = 15,
		Y = 0,
		X = ScreenWidth / 2,
		Centered = 1,
		ChainTransformation = BgStuff
	})
	
	local ls = 1 / 9 * ScreenHeight 
	local lx = ScreenHeight / 2 - ls / 2
	local l1 = - 1 / 9 * ScreenHeight
	local l2 = 1 / 9 * ScreenHeight

	BgStuff.Y = lx

	local sng = Global:GetSelectedSong()
	local d = 10

	ldFont = Fonts.TruetypeFont(GetSkinFile("font.ttf"));
	strAuthor = StringObject2D()
	strAuthor.ChainTransformation = BgStuff

	with (strAuthor, {
		Font = ldFont,
		FontSize = ls * 2 / 3,
		X = targBadge.X + targBadge.Width / 2 + 38,
		Y = 0 - ls * 2 / 3 + d,
		Layer = 16,
		Text = sng.Author,
		ChainTransformation = BgStuff
	})

	Engine:AddTarget(strAuthor)

	strSong = StringObject2D()
	with (strSong, {
		Font = ldFont,
		FontSize = ls * 2 / 3,
		X = targBadge.X + targBadge.Width / 2 + 38,
		Y = l1 - ls * 2 / 3 + d,
		Layer = 16,
		Text = sng.Title,
		ChainTransformation = BgStuff
	})

	Engine:AddTarget(strSong)

	local genre = Global:GetDifficulty(0).Genre 

	strGenre = StringObject2D()
	with (strGenre, {
		Font = ldFont,
		FontSize = ls * 2 / 3,
		X = targBadge.X + targBadge.Width / 2 + 38,
		Y = l2 - ls * 2 / 3 + d,
		Layer = 16,
		Text = genre,
		ChainTransformation = BgStuff
	})

	Engine:AddTarget(strGenre)

	BG = Engine:CreateObject()
	BG.Texture = "STAGEFILE" -- special constant
	BG.Centered = 1
	BG.X = ScreenWidth / 2
	BG.Y = ScreenHeight / 2
	
	local HRatio = ScreenHeight / BG.Height
	local VRatio = ScreenWidth / BG.Width
	
	BG.ScaleX = math.max(HRatio, VRatio)
	BG.ScaleY = math.max(HRatio, VRatio)
	BG.Layer = 10
	BG.Alpha = 0
	
	Phrases.Init()
end

function Cleanup()
end

function Update(Delta)
	Acceleration = Acceleration + Delta

	
	targBadge.Rotation = targBadge.Rotation + (6) 
end

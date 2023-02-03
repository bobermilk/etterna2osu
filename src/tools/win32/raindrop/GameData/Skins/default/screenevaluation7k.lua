game_require "TextureAtlas"
game_require "Histogram"
skin_require "Global/Background"
skin_require "Global/FadeInScreen"
skin_require "Scripts/ScoreDisplay"

function SetupFonts()
	EvalFont = Fonts.TruetypeFont(GetSkinFile("font.ttf"));
end

function GetRankImage(ScoreKeeper)
	local scorerank = ScoreKeeper.BMRank
	if scorerank == PMT_AAA then
		return "AAA"
	elseif scorerank == PMT_AA then
		return "AA"
	elseif scorerank == PMT_A then
		return "A"
	elseif scorerank == PMT_B then
		return "B"
	elseif scorerank == PMT_C then
		return "C"
	elseif scorerank == PMT_D then
		return "D"
	else
		return "F"
	end

end

function SetupRank(player)
	RankPic = Engine:CreateObject()
	RankPic.Texture = "Evaluation/score" .. GetRankImage(player.Scorekeeper) .. ".png"
	RankPic.Centered = 1
	RankPic.X = ScreenWidth / 2 - RankPic.Width / 2
	RankPic.Y = ScreenHeight / 2

	-- resize to something acceptable
	if RankPic.X < RankPic.Width / 2 then
		local Rat = (ScreenWidth / 2) / (RankPic.Width)
		RankPic:SetScale(Rat)
		RankPic.X = ScreenWidth / 2 - RankPic.Width / 2 * Rat
	end

	local str = ""
	if player.HasFailed then
		str = " (failed)"
	end

	RankStr = StringObject2D()
	RankStr.Text = "rank" .. str
	RankStr.X = RankPic.X - RankStr.TextSize / 2
	RankStr.Y = ScreenHeight / 2 + RankPic.Height / 2 + 10
	RankStr.Font = EvalFont
	RankStr.FontSize = 30
	Engine:AddTarget(RankStr)
end


function SetupJudgmentsDisplay(player)
  local ScoreKeeper = player.Scorekeeper
	JudgeStr = StringObject2D()
	JudgeStr.Font = EvalFont
	JudgeStr.FontSize = 26

	w0 = ScoreKeeper:GetJudgmentCount(SKJ_W0)
	w1 = ScoreKeeper:GetJudgmentCount(SKJ_W1)
	w2 = ScoreKeeper:GetJudgmentCount(SKJ_W2)
	w3 = ScoreKeeper:GetJudgmentCount(SKJ_W3)
	w4 = ScoreKeeper:GetJudgmentCount(SKJ_W4)
	w5 = ScoreKeeper:GetJudgmentCount(SKJ_MISS)
	Score = player.Score
	
	fmtext = ""
	if ScoreKeeper.UsesW0 == false then
		if ScoreKeeper.UsesO2 == false then
			fmtext = fmtext .. string.format("Flawless: %04d\nSweet: %04d\nNice: %04d\nWeak: %04d\nMiss: %04d", w1, w2, w3, w4, w5)
		else
			local p = ScoreKeeper.Pills
			fmtext = fmtext .. string.format("Flawless: %04d\nSweet: %04d\nNice: %04d\nMiss: %04d\nPills: %d", w1, w2, w3, w5, p)
		end
	else
		fmtext = fmtext .. string.format("Flawless*: %04d\nFlawless: %04d\nSweet: %04d\nNice: %04d\nOK: %04d\nMiss: %04d", w0, w1, w2, w3, w4, w5)
	end

	fmtext = fmtext .. string.format("\nMax Combo: %d", ScoreKeeper:GetScore(ST_MAX_COMBO))
	fmtext = fmtext .. string.format("\nNotes hit: %d%%", ScoreKeeper:GetPercentScore(PST_NH))
	fmtext = fmtext .. string.format("\nAccuracy: %d%%", ScoreKeeper:GetPercentScore(PST_ACC))
	fmtext = fmtext .. string.format("\nEX%%: %d%%", ScoreKeeper:GetPercentScore(PST_EX))
	fmtext = fmtext .. string.format("\nAverage hit (ms): %.2f" , ScoreKeeper.AvgHit)
	fmtext = fmtext .. string.format("\nStandard Deviation (ms): %.2f" , ScoreKeeper.StDev)
	fmtext = fmtext .. "\nraindrop rank: "

	if ScoreKeeper.Rank > 0 then
		fmtext = fmtext .. "+" .. ScoreKeeper.Rank
	else
		fmtext = fmtext .. ScoreKeeper.Rank
	end

	JudgeStr.Text = fmtext

	ScoreDisplay.X = ScoreDisplay.W / 2 + ScreenWidth / 2
	ScoreDisplay.Y = RankStr.Y + 30

	JudgeStr.X = ScoreDisplay.X
	JudgeStr.Y = ScreenHeight / 2 - RankPic.Height / 2

	Engine:AddTarget(JudgeStr)
end

function SetSongTitle(diff)
	Filter = Engine:CreateObject()
	Filter.Texture = "Global/filter.png"
	Filter.X = 0
	Filter.Y = ScreenHeight - 30
	Filter.Width = ScreenWidth
	Filter.Height = 40

	TitleText = StringObject2D()

	sng = Global:GetSelectedSong()
	if diff.Author ~= "" then
		difftxt = string.format("%s by %s", diff.Name, diff.Author)
	else
		difftxt = string.format("%s", diff.Name)
	end

	local Text = string.format ("%s by %s (Chart: %s)", Global:GetSelectedSong().Title, Global:GetSelectedSong().Author, difftxt)
	TitleText.Text = Text
	TitleText.Font = EvalFont
	TitleText.FontSize = 30

	TitleText.Y = ScreenHeight - 40
	TitleText.X = ScreenWidth / 2 - TitleText.TextSize / 2

	Engine:AddTarget(TitleText)
end

function SetupHistogram(p)
	histogram = Histogram:new(p)
	histogram:SetPosition(ScreenWidth / 2 - 255 / 2, 20)
	histogram:SetColor(30 / 255, 50 / 255, 200 / 255)
	hist_bg = histogram:SetBackground("Global/white.png")
	hist_bg.Red = 0.2
	hist_bg.Green = 0.2
	hist_bg.Blue = 0.2

	hStr = StringObject2D()
	hStr.Font = EvalFont
	hStr.FontSize = 26
	hStr.X = histogram.X
	hStr.Y = histogram.Y + histogram.Height
	hStr.Text = "histogram"
	Engine:AddTarget(hStr)
end

function Init()
  local p = Game:GetPlayer(0)
	BackgroundAnimation:Init()
	SetupFonts()
	SetupRank(p)
	SetupJudgmentsDisplay(p)

	sd = ScoreDisplay:new({Player = p})
	sd.Score = Score

	scoreStr = StringObject2D()
	scoreStr.Font = EvalFont
	scoreStr.FontSize = 36
	scoreStr.X = sd.X
	scoreStr.Y = sd.Y + sd.H
	scoreStr.Text = "score"

	Engine:AddTarget(scoreStr)

	SetSongTitle(p.Difficulty)
	SetupHistogram(p)
	ScreenFade.Init()
	ScreenFade.Out()

	displayWindows(p.Scorekeeper)
	displaySigma(p.Scorekeeper)
end

function displayWindows(sc)
	print ("judgment windows for current stage: ")
	for i=0,8 do 
		print(string.format("W%d: %d", i, sc:GetJudgmentWindow(i)))
	end
end

function displaySigma(sc)
	local indecaSigma = {}
	local decaSigma = sc.StDev / 10
	local totPoints = 0

	for i=-128,127 do
		local sigmaDecile = floor(math.abs(i) / decaSigma) + 1
		if not indecaSigma[sigmaDecile] then 
			indecaSigma[sigmaDecile] = 0
		end

		indecaSigma[sigmaDecile] = sc:GetHistogramPoint(i) + indecaSigma[sigmaDecile]
		totPoints = totPoints + sc:GetHistogramPoint(i)
	end

	for i=2, #indecaSigma do 
		indecaSigma[i] = indecaSigma[i] + indecaSigma[i - 1]
	end

	print ("total points: ", totPoints)
	for k,v in ipairs(indecaSigma) do 
		print (string.format("%.1f sigma (%04.2f ms): %.0f hits, %.2f%%", k / 10, sc.StDev * k / 10, v, v / totPoints * 100));
	end
end

function Cleanup()

end

function Update(Delta)
	sd:Run(Delta)
	BackgroundAnimation:Update(Delta)
end

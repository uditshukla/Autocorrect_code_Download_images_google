from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))

sentiment_analyzer_scores('''
© 2019 Copyright France 24 – All rights reserved. France 24 is not responsible for the content of external websites. Audience ratings certified by ACPM/OJD Date created : 08/05/2019 - 13:34 New Delhi (AFP) Former captain Kapil Dev Wednesday pegged India as one of the top three favourites to win the World Cup, which starts later this month, saying their pace bowling would come good in seaming English conditions. India open their campaign against South Africa on June 5 in Southampton with an eye on clinching their third title in the 50-over showpiece event. "Winning team looks like India, England and Australia and surprise package can be New Zealand," the Indian World Cup-winning skipper told reporters at a promotional event in New Delhi. "India has the combination of youth and experience. They have the right balance in four fast bowlers, three spinners and two big names in Virat Kohli and (M.S.) Dhoni," he said. India's pace battery is led by Jasprit Bumrah, the world's top bowler in the one-day format, and includes Mohammed Shami, Bhuvneshwar Kumar and Hardik Pandya. Bumrah has been hailed for his ability to bowl yorkers at the death, while Shami and Kumar have also impressed. "They are fantastic, very good. English conditions will help them. They can swing the ball," said Dev, known as "Haryana Hurricane" during his playing days for his pace. "They have Bumrah and Shami who can bowl 145 (kmph) plus. So we have swing, we have pace. That's a very good combination to have." Dev, who led India to their maiden World Cup in 1983 when his side beat two-time champions West Indies to take the trophy at Lord's, said it was the "belief" which separated winners from the rest. Dev slammed comparisons between him and star all-rounder Pandya who has impressed with his power hitting in the team's middle order and skills as a medium-pace bowler. The 25-year-old Pandya, who is set to play his first 50-over World Cup, has earned his place in the Indian XI with 731 runs and 44 wickets in 45 ODIs since making his debut in 2016. "He is an upcoming player... Please do not pressure him. He is a young talent, let him play his cricket with his own free mind," said Dev. When quizzed about the on-field chemistry between former captain Dhoni and Kohli, Dev said both the players were crucial to India's World Cup hopes. "Both the cricketers have done so well for India, unmatchable. First, all of them should understand that they are not playing for themselves but playing for the country." ? 2019 AFP The page no longer exists or did not exist at all. Please check the address or use the links below to access the requested content.
                          ''')
from game import ProblemGenerator as pg
import os

PG_METHODS = [pg.square5,pg.random2x2,pg.random3x3, pg.near100, pg.reverses, pg.square50, pg.unitsdigit]

# ROJO_MUSIC = map(os.path.join,'sounds',[f'Rojo ({i}).mp3' for i in range(1,11)])
ROJO_MUSIC = [os.path.join('sounds',f'Rojo ({i}).mp3') for i in range(1,11)]

house_of_rising_sun = """There is a house in New Orleans
They call the Rising Sun
And it's been the ruin of many a poor boy
Dear God, I know I was one
My mother was a tailor
She sewed my new blue jeans
And my father was a gamblin' man
Way down in New Orleans
And the only thing a gambler needs
Is a suitcase in the trunk
And the only time he's satisfied
Is when he's on a drunk
Oh mother, tell your children
Not to do what I have done
Don't spend your life in sin and misery
In the House of the Rising Sun
I got one foot on the platform
And another on the train
And I'm goin' back to New Orleans
To wear that ball and chain
There is a house in New Orleans
They call the Rising Sun
And it's been the ruin of many a poor boy
Dear God, I know I was one
Dear God, I know I was the one"""
# TwelveShogi_AlphaZero

Training is in progress.

A simplified version of Shogi with the AI is trained by alpha-zero-type training method

This project is based on these main resources:

1) DeepMind's Oct 19th publication: [Mastering the Game of Go without Human Knowledge](https://www.nature.com/articles/nature24270.epdf?author_access_token=VJXbVjaSHxFoctQQ4p2k4tRgN0jAjWel9jnR3ZoTv0PVW4gB86EEpGqTRDtpIz-2rmo8-KG06gqVobU5NSCFeHILHcVFUeMsbvwS-lxjqQGg98faovwjxeTUgZAUMnRQ).
2) The <b>great</b> Gomoku development of the DeepMind ideas that @junxiaosong did in his repo: https://github.com/junxiaosong/AlphaZero_Gomoku
3) The <b>wonderful</b> Chess development of the DeepMind ideas that @Zeta36 did in his repo:
https://github.com/Zeta36/chess-alpha-zero/
4) The <b>brilliant</b> Reversi development of the DeepMind ideas that @mokemokechicken did in his repo: https://github.com/mokemokechicken/reversi-alpha-zero
5) DeepMind just released a new version of AlphaGo Zero (named now AlphaZero) where they master chess from scratch: 
https://arxiv.org/pdf/1712.01815.pdf.

# TwelveShogi

TwelveShogi comes from the TV series -- The Genius:_Black_Garnet (https://en.wikipedia.org/wiki/The_Genius:_Black_Garnet) in which named as "Twelve Jangqi". The board is looked like follows:

![image](http://github.com/PlanetMoon/TwelveShogi_AlphaZero/raw/master/BMP/board_snapshot.jpg)

The rules list as follows:

The game played by two players. We defined the player move direction is the player's color which means the top side player is playing down color and the down side player is playing up color.

All shogimans can only move one grid by one step at any direction. Any shogiman that has been catched is put in the prison. The prisoners can be put in the board instead of move a shogiman. However, the prisoners cannot be put at the opposite colored area(which means the opposite side's bottom row).

Zi(子): can only go forward. And when the Zi reached the opposite colored area it will be promoted to Hou(侯)

Jiang(将): can go forward, back, left and right.

Xiang(相): can go NW, NE, SW and SE.

Wang(王): can go every direction.

Hou(侯): can go any direction except SW and SE for up color.

Tips: every shogiman has little pots in the pictures which represent the directions where the shogiman can move to.

The game is end when the Wang is catched by the other player or the Wang reached the opposite colored area and live for a round or tie when 40 moves are taken by two players together(I defined it, can be changed).

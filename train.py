# -*- coding: utf-8 -*-
"""
@author: Xingye Xu
""" 

from __future__ import print_function
import random
import datetime
import numpy as np
import pickle
from collections import defaultdict, deque
from ShogiBoard import *
from ShogiGlobal import *
from PolicyValueNet import *
from mcts_pure import MCTSPlayer as MCTS_Pure
from mcts import MCTSPlayer

def start_play(board, player1, player2, startPlayer=0):
    """
    start a game between two players
    """
    board.resetBoard()
    if startPlayer not in (0,1):
        raise Exception('startPlayer should be 0 (up) or 1 (down)')
    p1 = startPlayer
    p2 = 1 - startPlayer
    if p1:
        print("train-start_play: startPlayer is pure mcts")
    else:
        print("train-start_play: startPlayer is mcts")
    player1.set_player_ind(p1)
    player2.set_player_ind(p2)
    players = {p1: player1, p2: player2}
    board.printBoard()
    while(1):
        currentPlayer = board.curStepColor
        playerInTurn = players[currentPlayer]
        move = playerInTurn.get_action(board)
        result = board.doMove(move)
        board.printBoard()
        if result > 0:
            if result == p1 + 1:
                print("train-start_play: winner is p1")
                return 1
            elif result == p2 + 1:
                print("train-start_play: winner is p2")
                return 2
            else:
                print("train-start_play: tie")
                return 0           
            
def start_self_play(board, player, temp=1e-3):
    """ start a self-play game using a MCTS player, reuse the search tree
    store the self-play data: (state, mcts_probs, z)
    """
    board.resetBoard()
    p1 = 0
    p2 = 1
    states, mctsProbs, currentPlayers = [], [], []
    moveCounts = 0
    while(1):
        moveCounts = moveCounts + 1
        move, moveProbs = player.get_action(board, temp=temp, return_prob=1)
        writeTrainingLog("train-start_self_play: curColor = %d, moveCounts = %d" % (board.curStepColor, moveCounts))
        writeTrainingLog("train-start_self_play: move = %d %d %d %d %d" % (board.board[move//72, move%72//12].kind, move // 72, move % 72 // 12, move % 12 // 3, move % 12 % 3))
        # store the data
        states.append(board.currentState())
        mctsProbs.append(moveProbs)
        currentPlayers.append(board.curStepColor)
        # perform a move
        result = board.doMove(move)
        if result > 0:
            # winner from the perspective of the current player of each state
            winners_z = np.zeros(len(currentPlayers))  
            if result != 3:
                winners_z[np.array(currentPlayers) == result - 1] = 1.0
                winners_z[np.array(currentPlayers) != result - 1] = -1.0
                winner = result
            else:
                winner = 0
            #reset MCTS root node
            player.reset_player() 
            return winner, moveCounts, zip(states, mctsProbs, winners_z)
            
class TrainPipeline():
    def __init__(self):
        # params of the board and the game
        self.board_width = 6
        self.board_height = 6
        self.n_in_row = 4
        self.board = ShogiBoard()
        # training params 
        self.learn_rate = 5e-3
        self.lr_multiplier = 1.0  # adaptively adjust the learning rate based on KL
        self.temp = 1.0 # the temperature param
        self.n_playout = 400 # num of simulations for each move
        self.c_puct = 5
        self.buffer_size = 10000
        self.batch_size = 512 # mini-batch size for training
        self.data_buffer = deque(maxlen=self.buffer_size)        
        self.play_batch_size = 1 
        self.epochs = 5 # num of train_steps for each update
        self.kl_targ = 0.025
        self.check_freq = 50 
        self.game_batch_num = 3000
        self.best_win_ratio = 0.0
        # num of simulations used for the pure mcts, which is used as the opponent to evaluate the trained policy
        self.pure_mcts_playout_num = 1000  
        # start training from a given policy-value net
#        policy_param = pickle.load(open('current_policy.model', 'rb')) 
#        self.policy_value_net = PolicyValueNet(self.board_width, self.board_height, net_params = policy_param)
        # start training from a new policy-value net
        self.policy_value_net = PolicyValueNet() 
        self.mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn, c_puct=self.c_puct, n_playout=self.n_playout, is_selfplay=1)
                
    def collect_selfplay_data(self, n_games=1):
        """collect self-play data for training"""
        for i in range(n_games):
            winner, stepCounts, play_data = start_self_play(self.board, self.mcts_player, temp=self.temp)
            print("train-collect_selfplay_data: winner = %d" % winner)
            self.episode_len = stepCounts 
            self.data_buffer.extend(play_data)
                        
    def policy_update(self):
        """update the policy-value net"""
        mini_batch = random.sample(self.data_buffer, self.batch_size)
        state_batch = [data[0] for data in mini_batch]
        mcts_probs_batch = [data[1] for data in mini_batch]
        winner_batch = [data[2] for data in mini_batch]            
        old_probs, old_v = self.policy_value_net.policy_value(state_batch) 
        for i in range(self.epochs): 
            loss, entropy = self.policy_value_net.train_step(state_batch, mcts_probs_batch, winner_batch, self.learn_rate*self.lr_multiplier)
            new_probs, new_v = self.policy_value_net.policy_value(state_batch)
            kl = np.mean(np.sum(old_probs * (np.log(old_probs + 1e-10) - np.log(new_probs + 1e-10)), axis=1))  
            if kl > self.kl_targ * 4:   # early stopping if D_KL diverges badly
                break
        # adaptively adjust the learning rate
        if kl > self.kl_targ * 2 and self.lr_multiplier > 0.1:
            self.lr_multiplier /= 1.5
        elif kl < self.kl_targ / 2 and self.lr_multiplier < 10:
            self.lr_multiplier *= 1.5
            
        explained_var_old =  1 - np.var(np.array(winner_batch) - old_v.flatten())/np.var(np.array(winner_batch))
        explained_var_new = 1 - np.var(np.array(winner_batch) - new_v.flatten())/np.var(np.array(winner_batch))        
        print("kl:{:.5f},lr_multiplier:{:.3f},loss:{},entropy:{},explained_var_old:{:.3f},explained_var_new:{:.3f}".format(
                kl, self.lr_multiplier, loss, entropy, explained_var_old, explained_var_new))
        return loss, entropy
        
    def policy_evaluate(self, n_games=10):
        """
        Evaluate the trained policy by playing games against the pure MCTS player
        Note: this is only for monitoring the progress of training
        """
        current_mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn, c_puct=self.c_puct, n_playout=self.n_playout)
        pure_mcts_player = MCTS_Pure(c_puct=5, n_playout=self.pure_mcts_playout_num)
        win_cnt = defaultdict(int)
        for i in range(n_games):
            print("train-policy_evaluate: game = %d" % (i))
            winner = start_play(self.board, current_mcts_player, pure_mcts_player, startPlayer=i%2)
            win_cnt[winner] += 1
        win_ratio = 1.0*(win_cnt[1] + 0.5*win_cnt[0])/n_games
        print("num_playouts:{}, win: {}, lose: {}, tie:{}".format(self.pure_mcts_playout_num, win_cnt[1], win_cnt[2], win_cnt[0]))
        return win_ratio
    
    def run(self):
        """run the training pipeline"""
        try:
            curTime = datetime.datetime.now()
            writeTrainingLog("train-run: {}".format(curTime))
            for i in range(self.game_batch_num):
                print("train-run: train round %d" % i)
                writeTrainingLog("train-run: train round %d" % i)
                self.collect_selfplay_data(self.play_batch_size)
                print("batch i:{}, episode_len:{}".format(i+1, self.episode_len))
                writeTrainingLog("batch i:{}, episode_len:{}".format(i+1, self.episode_len))
                print("train-run: len of data_buffer = {}".format(len(self.data_buffer)))
                if len(self.data_buffer) > self.batch_size:
                    loss, entropy = self.policy_update()                    
                # check the performance of the current model，and save the model params
                if (i+1) % self.check_freq == 0:
                    print("current self-play batch: {}".format(i+1))
                    writeTrainingLog("current self-play batch: {}".format(i+1))
                    win_ratio = self.policy_evaluate()
                    net_params = self.policy_value_net.get_policy_param() # get model params
                    pickle.dump(net_params, open('current_policy.model', 'wb')) # save model param to file
                    if win_ratio > self.best_win_ratio: 
                        print("New best policy!!!!!!!!")
                        writeTrainingLog("New best policy!!!!!!!!")
                        self.best_win_ratio = win_ratio
                        pickle.dump(net_params, open('best_policy.model', 'wb')) # update the best_policy
                        if self.best_win_ratio == 1.0 and self.pure_mcts_playout_num < 5000:
                            self.pure_mcts_playout_num += 1000
                            self.best_win_ratio = 0.0
        except KeyboardInterrupt:
            print('\n\rquit')
            writeTrainingLog('\n\rquit')
    

if __name__ == '__main__':
    training_pipeline = TrainPipeline()
    training_pipeline.run()    
    

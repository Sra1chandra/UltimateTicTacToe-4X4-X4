import sys
import random
import signal
import time
import copy

class Player73():
	def __init__(self):
		self.count=0;
		self.depth=4;
		self.ply='x';
		pass
	def move(self, board, old_move, flag):
		self.ply=flag;
		self.count=0;
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		cells = board.find_valid_move_cells(old_move)
		total_possible_ways=len(cells);
		x=sum([2,3,4])
		if total_possible_ways==256:
			return cells[random.randrange(len(cells))];
		#self.assign_utility(board,old_move,flag);
		#if self.count==50:
		#	temp=self(minmax)
		temp = self.minmax(board,old_move,flag);
		#print temp
		# if self.count<500:
		# 	self.depth=5;
		# if self.count>4000:
		# 	self.depth=4;
		# print str(self.count)+" "+str(self.depth)+" "+str(temp)
		return temp;

	def assign_value(self,row):
		row_o=row.count('o');
		row_x=row.count('x');
		temp_heuristic=0;
		if row_o==0:
			if row_x==1:
				temp_heuristic+=1;
			if row_x==2:
				temp_heuristic+=20;
			if row_x==3:
				temp_heuristic+=200;
		if row_x==0:
			if row_o==1:
				temp_heuristic-=1;
			if row_o==2:
				temp_heuristic-=20;
			if row_o==3:
				temp_heuristic-=200;
		return temp_heuristic;

	def assign_utility1(self,row,block_row):
		heuristic=0;
		if block_row.count('o')==0 and block_row.count('d')==0:
			if block_row.count('x')==3:
				heuristic+=int(150*int(sum(row)));
			# if block_row.count('x')==2:
			# 	heuristic+=int(2*int(sum(row)));
			# if block_row.count('x')==1:
			# 	heuristic+=int(1*int(sum(row)));
		if block_row.count('x')==0 and block_row.count('d')==0:
			if block_row.count('o')==3:
				heuristic+=int(150*int(sum(row)));
			# if block_row.count('o')==2:
			# 	heuristic+=int(2*int(sum(row)));
			# if block_row.count('o')==1:
			# 	heuristic+=int(1*int(sum(row)));

		return int(heuristic)


	def assign_utility(self,board,old_move,flag):
		block=board.block_status;
		b=board.board_status;
		temp_score=[[0 for i in range(4)] for j in range(4)]
		temp_block=[['-' for i in range(4)] for j in range(4)]
		heuristic=0;
		draw_heuristic=0;
		cntx = 0
		cnto = 0
		cntd = 0
		for block_row in range(4):
			for block_col in range(4):
				temp_heuristic=0;
				if block[block_row][block_col] == 'x':
					cntx += 1
					temp_heuristic=1500;
				if block[block_row][block_col] == 'o':
					cnto += 1
					temp_heuristic=-1500;
				if block[block_row][block_col] == 'd':
					cntd += 1
					temp_heuristic=0;
				if block[block_row][block_col] == '-':
					for i in range(4):
						for j in range(4):
							temp_block[i][j]=b[block_row*4+i][block_col*4+j]
					#print temp;
					for i in range(4):
						row = temp_block[i]							#i'th row
						col = [x[i] for x in temp_block]			#i'th column
						#print row,col
						temp_heuristic+=self.assign_value(row);
						temp_heuristic+=self.assign_value(col);
					diagonal=[];
					for i in range(4):
						diagonal.append(temp_block[i][i]);
					temp_heuristic+=self.assign_value(diagonal);
					diagonal=[];
					for i in range(4):
						diagonal.append(temp_block[i][3-i]);
					temp_heuristic+=self.assign_value(diagonal);
					temp_score[block_row][block_col]=temp_heuristic
				draw_heuristic+=temp_heuristic;
		heuristic=0;
		for i in range(4):
			for j in range(4):
				row = temp_score[i]							#i'th row
				col = [x[i] for x in temp_score]			#i'th column
				block_row = block[i]							#i'th row
				block_col = [x[i] for x in block]			#i'th column
				heuristic+=self.assign_utility1(row,block_row);
				heuristic+=self.assign_utility1(col,block_col);
		diagonal=[];
		block_diagonal=[];
		for i in range(4):
			diagonal.append(temp_score[i][i]);
			block_diagonal.append(block[i][i]);
		heuristic+=self.assign_utility1(diagonal,block_diagonal);
		diagonal=[];
		block_diagonal=[];
		for i in range(4):
			diagonal.append(temp_score[3-i][i]);
			block_diagonal.append(block[3-i][i]);
		heuristic+=self.assign_utility1(diagonal,block_diagonal);

		if heuristic==0:
			heuristic=draw_heuristic;
		if self.ply=='o':
			heuristic=-heuristic;
		return heuristic

	def minmax(self,board,old_move,flag):
		cells = board.find_valid_move_cells(old_move)
		total_possible_ways=len(cells);
		# if total_possible_ways>30:
		# 	self.depth=2;
		depth=0;
		maxvalue=-sys.maxint
		maxindex=0
		alpha=-sys.maxint
		beta=sys.maxint
		req=[];
		self.count+=1;
		for i in range(total_possible_ways):
			#print cells[i];
			new_move=cells[i];
			temp=self.min_step(board,old_move,new_move,depth,flag,alpha,beta);
			alpha=max(alpha,temp)
			if maxvalue<temp:
				maxvalue=temp;
				maxindex=i;
			if maxvalue==temp:
				#print i
				req.append(i)
			if alpha>=beta:
				break;
		# return cells[maxindex];
		return cells[req[random.randrange(len(req))]];


	def min_step(self,board,old_move,new_move,depth,flag,alpha,beta):
		self.count+=1;
		temp_board=copy.deepcopy(board);
		temp_board.update(old_move,new_move,flag);
		state=temp_board.find_terminal_state()
		if state[1]=='WON':
			if self.ply==state[0]:
				return 1000000;
			else:
				return -1000000;
		if state[1]=='DRAW':
			return 0;
		cells = temp_board.find_valid_move_cells(new_move)
		total_possible_ways=len(cells);
		if total_possible_ways>=40:
			depth=depth+1;
		mini=sys.maxint
		depth=depth+1;

		if depth>=self.depth:
			temp= self.assign_utility(temp_board,old_move,flag)
			#temp=random.randrange(1,1000)
			#print temp
			return temp

		if flag=='x':
			flag='o';
		elif flag=='o':
			flag='x';

		for i in range(total_possible_ways):
			move=cells[i];
			#self.max_step(temp_board,new_move,move,1,flag)
			temp=self.max_step(temp_board,new_move,move,depth,flag,alpha,beta);
			beta=min(beta,temp)
			mini=min(mini,temp)
			if alpha>=beta:
				break;
		return mini;

	def max_step(self,board,old_move,new_move,depth,flag,alpha,beta):
		self.count+=1;
		temp_board=copy.deepcopy(board);
		temp_board.update(old_move,new_move,flag);
		state=temp_board.find_terminal_state()
		if state[1]=='WON':
			if self.ply==state[0]:
				return 1000000;
			else:
				return -1000000;
		if state[1]=='DRAW':
			return 0;

		#print temp_board.board_status
		cells = temp_board.find_valid_move_cells(new_move)
		total_possible_ways=len(cells);
		maxi = -sys.maxint
		if total_possible_ways>40:
			depth=depth+1;
		depth=depth+1;

		if depth>=self.depth:
			#temp=random.randrange(1,1000)
			temp=self.assign_utility(temp_board,old_move,flag)
			return temp

		if flag=='x':
			flag='o';
		elif flag=='o':
			flag='x';
		for i in range(total_possible_ways):
			move=cells[i];
			temp=self.min_step(temp_board,new_move,move,depth,flag,alpha,beta);
			alpha=max(alpha,temp)
			maxi=max(maxi,temp)
			if alpha>=beta:
				break;
		return maxi;

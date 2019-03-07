#!/usr/bin/python3
"""Milestone_A_who_and_what.py
This runnable file will provide a representation of
answers to key questions about your project in CSE 415.

"""

# DO NOT EDIT THE BOILERPLATE PART OF THIS FILE HERE:

CATEGORIES=['Baroque Chess Agent','Feature-Based Reinforcement Learning for the Rubik Cube Puzzle', \
            'Hidden Markov Models: Algorithms and Applications']

class Partner():
    def __init__(self, lastname, firstname, uwnetid):
        self.uwnetid=uwnetid
        self.lastname=lastname
        self.firstname=firstname

    def __lt__(self, other):
        return (self.lastname+","+self.firstname).__lt__(other.lastname+","+other.firstname)

    def __str__(self):
        return self.lastname+", "+self.firstname+" ("+self.uwnetid+")"

class Who_and_what():
    def __init__(self, team, option, title, approach, workload_distribution, references):
        self.team=team
        self.option=option
        self.title=title
        self.approach = approach
        self.workload_distribution = workload_distribution
        self.references = references

    def report(self):
        rpt = 80*"#"+"\n"
        rpt += '''The Who and What for This Submission

Project in CSE 415, University of Washington, Winter, 2019
Milestone A

Team: 
'''
        team_sorted = sorted(self.team)
        # Note that the partner whose name comes first alphabetically
        # must do the turn-in.
        # The other partner(s) should NOT turn anything in.
        rpt += "    "+ str(team_sorted[0])+" (the partner who must turn in all files in Catalyst)\n"
        for p in team_sorted[1:]:
            rpt += "    "+str(p) + " (partner who should NOT turn anything in)\n\n"

        rpt += "Option: "+str(self.option)+"\n\n"
        rpt += "Title: "+self.title + "\n\n"
        rpt += "Approach: "+self.approach + "\n\n"
        rpt += "Workload Distribution: "+self.workload_distribution+"\n\n"
        rpt += "References: \n"
        for i in range(len(self.references)):
            rpt += "  Ref. "+str(i+1)+": "+self.references[i] + "\n"

        rpt += "\n\nThe information here indicates that the following file will need\n"+ \
               "to be submitted (in addition to code and possible data files):\n"
        rpt += "    "+ \
               {'1':"Baroque_Chess_Agent_Report",'2':"Rubik_Cube_Solver_Report", \
                '3':"Hidden_Markov_Models_Report"} \
                   [self.option]+".pdf\n"

        rpt += "\n"+80*"#"+"\n"
        return rpt


# END OF BOILERPLATE.

# Change the following to represent your own information:

stephan = Partner("Hagel", "Stephan", "sthagel")
palash = Partner("Roychowdhury", "Palash", "palashrc")
team = [stephan, palash]

OPTION = '2'
# Legal options are 1, 2, and 3.

title = "A twist of faith."

approach = '''We will work with a 2x2x2 Rubik's cube to significantly reduce the size of the state space.
              We will use Q-Learning and deep learning to solve the puzzle. Furthermore, we use the method of
              curriculum learning, which iteratively gives the algorithm states, which need more moves to be solved.
              Our goal is to bring the algorithm as close to solving the cube optimally, that is in 11 or less moves
              (11 is the so called "God\'s number" for the 2x2x2 cube).'''

workload_distribution = '''Palash will focus on implementing and optimizing the curriculum learning method. 
                           Stephan will focus on the general Q-Learning implementation.
                           Both will work closely together to use deep learning methods to improve the algorithm.'''

reference1 = '''"Deep Q-Learning for Rubik’s Cube", by Etienne Simon and Eloi Zablocki
    URL: https://github.com/EloiZ/DeepCube'''

reference2 = '''"Artificial Intelligence: Foundations of Computational Agents", 2nd Edition by  David L. Poole and Alan 
    K. Mackworth available online at: https://artint.info/2e/html/ArtInt2e.html'''

our_submission = Who_and_what([stephan, palash], OPTION, title, approach, workload_distribution,
                              [reference1, reference2])

# You can run this file from the command line by typing:
# python3 who_and_what.py

# Running this file by itself should produce a report that seems correct to you.
if __name__ == '__main__':
    print(our_submission.report())

#I have taken ideas from sources available on various university sites
#the idea for this code is heavily inspired from Computational Geometry by Prof. Mark de Berg
#the code is however completely mine
class node(object):#initialising a node
    def __init__(self,k):
        self.val=k
        self.lsub=None;self.rsub=None;self.yvalues=[]#the node has attributes left subtree, right subtree, list which stores y values of all the nodes beneath it
def lb(l,y1):#finding the smallest index in a list which has y coordinate>=y1
    if len(l)==0:
        return None
    else:
        a=0;b=len(l)-1
        while (b-a)>1:
            mid=(a+b)//2
            if l[mid][1]>=y1:
                b=mid
            else:
                a=mid
        if l[a][1]>=y1:
            return a
        elif l[b][1]>=y1:
            return b
        else:
            return None

def ub(l,y2):#finding the largest index in a list which has y coordinate <=y2
    #this is simple binary search so takes O(log(n)) time
    if len(l)==0:
        return None
    else:
        a=0;b=len(l)-1
        while (b-a)>1:
            mid=(a+b)//2#mid value
            if l[mid][1]>y2:#contracting the search length by 2 times in each step 
                b=mid
            else:
                a=mid
        
        if l[b][1]<=y2:
            return b
        elif l[a][1]<=y2:
            return a
        else:
            return None

def s1dy(l,y1,y2):#giving a list of all points which have y coordinates between y1 and y2
    ans=[]
    i=lb(l,y1);j=ub(l,y2)#the lower and upper bounds for indices respectively
    if i==None or j==None:
        return []
    else:
        for i1 in range (i,j+1):
            ans.append(l[i1])
        return ans
    
def sli(l,i,j):#a function which returns the slice of a list from i to j-1
    #its function is same as slicer but with reduces time complexity
    ans=[]
    for i1 in range (i,j):
        ans.append(l[i1])
    return ans


def isleaf(a):#this simply checks if a node is a leaf or not
    if a==None:#node itself is non existent
        return False
    if a.lsub==None and a.rsub==None:
        return True
    return False


def avl(l):#building an AVL tree without rotation
    #we dont need rotation as we will slice the data by exactly a factor of half
    n=len(l);median=n//2
    if n==0:
        None
    elif n==1:
        u=node(l[0])
        return u
    else:
        #tree property: every node is the median of all the nodes beneath it(including itself)
        root=node(l[median])
        root.lsub=avl(sli(l,0,median))
        root.rsub=avl(sli(l,median+1,n))
        return root

    
def avl2dh(l):#building a helper function which sorts according to x and y coordinates
    lx=sorted(l);n=len(l)
    ly=sorted(l, key=lambda x:x[1])
    return lx,ly


def avl2d(lx,ly):#this basically adds y subtrees to the AVL tree of x coordinates
    #property of tree: x coordinate's property is same as the AVL tree built earlier
    #But every node also stores data of all coordinates sorted according to y in its subtree
    if len(lx)!=len(ly):#ust to check if a flaw is there
        print('glitch')
    if len(lx)==0:
        return None
    if len(lx)==1:#only one value of x
        u=node(lx[0])
        u.yvalues=[ly[0]]
        return u
    else:
        root=node(lx[len(lx)//2])#the median value
        root.yvalues=ly#values of y contained in the nodes subtree
        yl=[];yr=[]
        for i in ly:
            if i[0]<lx[len(lx)//2][0]:#coordinates which will go in the left subtree
                yl.append(i)
            elif i[0]>lx[len(lx)//2][0]:
                yr.append(i)
        root.lsub=avl2d(sli(lx,0,len(lx)//2),yl)#recursively constructing the tree
        root.rsub=avl2d(sli(lx,len(lx)//2+1,len(lx)),yr)
        return root

    
def fsn(a,x1,x2):#finds the first nodes whose x coordinates is in the given range
    if a==None:
        return None
    v=a
    while isleaf(v)!=True and v!=None:
        if v.val[0]<=x2 and v.val[0]>=x1:
            #if values is in the range simply return it
            return v
            break
        else:
            if v.val[0]<=x1:
                v=v.rsub#if the current node is smaller, check from its right subtree(which will be obvoiously greater than the left one)
            else:
                v=v.lsub
    if v==None:
        return None
    if v.val[0]<=x2 and v.val[0]>=x1:
        #print(v.val,v.lsub.val,v.rsub.val)
        return v
    else:
        return None


def s2d(a,x1,x2,y1,y2):
    #searching the X-Y plane
    ans=[]#it will store the valid coordinates
    v=fsn(a,x1,x2)#node nearest from the root which has the values of x coordinate in the desired range
    #obvously all the other valid x coordinates will be in the subtrees of x
    if v==None:#no valid node
        return ans
    lv=v.lsub;rv=v.rsub#the right and left subtree of the symbolic node respectively
    if isleaf(v):#check if v is a leaf
        if v.val[0]>=x1 and v.val[0]<=x2 and v.val[1]>=y1 and v.val[1]<=y2:#check if the x and y coordinates are valid
            ans.append(v.val)#if yes, simply append it in the answer list
            return [v.val]
        else:
            return []
    else:
        if v.val[0]>=x1 and v.val[0]<=x2:#if the node v has valid x coordinates
            if v.val[1]>=y1 and v.val[1]<=y2:#it also has valid y coordintes
                ans.append(v.val)#as this coordinate is valid append it in the ans
        while lv!=None:#traversing the left subtree of v
            if lv.val[0]>=x1 and lv.val[0]<=x2 and lv.val[1]>=y1 and lv.val[1]<=y2:#a valid node
                ans.append(lv.val)#append it in the ans
            if lv.val[0]>=x1:#if x coordinate of lv is valid, then all values between lv and v are valid automatically
                if lv.rsub!=None:#if right subtree is empty, no point in traversing it
                    for i in s1dy(lv.rsub.yvalues,y1,y2):#simply checking all the y coordinates of the right subtree will do, as all the x coordinates are automatically
                        #valif from the above conditions
                        ans.append(i)
                lv=lv.lsub
            else:#the right subtree is empty or x coordinate of lv is invalid(its too small)
                #so we increase the value by going in the right (in the hope that we get the values of x in range
                lv=lv.rsub
        while rv!=None:#similar arguments as in the left subtree
            if rv.val[0]>=x1 and rv.val[0]<=x2 and rv.val[1]>=y1 and rv.val[1]<=y2:
                ans.append(rv.val)
            if rv.val[0]<=x2:
                if rv.lsub!=None:
                    for i in s1dy(rv.lsub.yvalues,y1,y2):
                        ans.append(i)
                rv=rv.rsub
            else:
                rv=rv.lsub
        return ans
            

def s2(a,p1,p2,d):#a simple shortcut function
    return s2d(a,p1-d,p1+d,p2-d,p2+d)

class PointDatabase:#declaring the class as required in the assignment
    def __init__(self,l):#initialising the database
        lx=avl2dh(l)[0];ly=avl2dh(l)[1]
        self.tree=avl2d(lx,ly)
    def searchNearby(self,p,d):#making the desired function
        return s2d(self.tree,p[0]-d,p[0]+d,p[1]-d,p[1]+d)

'''a=avl2dh([(1,6),(2,4),(3,7),(4,9),(5,1),(6,3),(7,8),(8,10),(9,2),(10,5)])
ref=avl2d(a[0],a[1])'''


        
    
            
            
    

    
    
        
        

            

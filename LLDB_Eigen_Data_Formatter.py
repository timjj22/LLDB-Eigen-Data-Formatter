import lldb
import os

def __lldb_init_module (debugger, dict):
    debugger.HandleCommand("type summary add -x \"Eigen::PlainObjectBase\" -F LLDB_Eigen_Data_Formatter.format")

# Define a context manager to suppress stdout and stderr.
#  see http://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions
class suppress_stdout_stderr(object):
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (os.dup(1), os.dup(2))

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close the null files
        os.close(self.null_fds[0])
        os.close(self.null_fds[1])

def evaluate_expression(valobj, expr):
    return valobj.GetProcess().GetSelectedThread().GetSelectedFrame().EvaluateExpression(expr)    

def format (valobj,internal_dict):
    
    # Print out the previous data as well
    print(str(valobj.GetValueForExpressionPath("")))
        
    # fetch data (For fixed sized arrays only)
    data = valobj.GetValueForExpressionPath(".m_storage.m_data.array")
    num_data_elements = data.GetNumChildren()
    is_fixed_size = 1

    if not data.IsValid():
        # is dynamically sized array, deal with results slightly differently
        data = valobj.GetValueForExpressionPath(".m_storage.m_data")
        #num_data_elements = valobj.GetValueForExpressionPath(".m_storage.m_rows").GetValueAsSigned() * valobj.GetValueForExpressionPath(".m_storage.m_cols").GetValueAsSigned()
        is_fixed_size = 0


    # determine expression path of the current valobj
    stream = lldb.SBStream()
    valobj.GetExpressionPath(stream)
    valobj_expression_path = stream.GetData()
    
    # determine rows and cols
    rows = cols = 0
    with suppress_stdout_stderr():
        rows = evaluate_expression(valobj, valobj_expression_path+".rows()").GetValueAsSigned()
        cols = evaluate_expression(valobj, valobj_expression_path+".cols()").GetValueAsSigned()
        #rows = lldb.frame.EvaluateExpression(valobj_expression_path+".rows()").GetValueAsSigned()
        #cols = lldb.frame.EvaluateExpression(valobj_expression_path+".cols()").GetValueAsSigned()
        
        #print(valobj.CreateValueFromExpression("bla", valobj_expression_path+".rows()"))
    
    output = ""

    # check that the data layout fits a regular dense matrix
    if is_fixed_size and rows*cols != num_data_elements:
      print("error: eigen data formatter: could not infer data layout. printing raw data instead")
      print("ROWS: " + str(rows) + " COLS: " + str(cols) + " elements: " + str(num_data_elements))
      cols = 1
      rows = num_data_elements

    # print matrix dimensions
    output += "rows: " + str(rows) + ", cols: " + str(cols)

    # determine padding
    padding = 1
    # don't print too many items
    max_element_count = 25
    
    if is_fixed_size:
        for i in range(0, min(data.GetNumChildren(), rows*cols)):
            padding = max(padding, len(str(data.GetChildAtIndex(i).GetValue())))
    else:
        for j in range(0, min(rows, max_element_count)):
            for i in range(0, min(cols, max_element_count)):
                padding = max(padding, len(str(data.GetChildAtIndex(j + i*rows, 0, True).GetValue())))

    # print values
    for j in range(0,min(rows, max_element_count)):
        if j is 0:
            output += "\n["
        for i in range(0,min(cols, max_element_count)):
            #val = data.GetChildAtIndex(j+i*cols, lldb.eNoDynamicValues, True).GetValue()
            output += data.GetChildAtIndex(i*rows + j, 0, True).GetValue().rjust(padding+1, ' ')
        
        if j!=rows-1:
            output += " ]\n["
        if j == rows-1:
            output += " ]"

    return output

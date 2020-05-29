
#strategy for checking if a given indicator, or just anything rly crosses over shit 
#credit:quantnews

def CrossesOver(stream1, stream2):
    # If stream2 is an int or float, check if stream1 has crossed over that fixed number
    if isinstance(stream2, int) or isinstance(stream2, float):
        if stream1[len(stream1)-1] <= stream2:
            return False
        else:
            if stream1[len(stream1)-2] > stream2:
                return False
            elif stream1[len(stream1)-2] < stream2:
                return True
            else:
                x = 2
                while stream1[len(stream1)-x] == stream2:
                    x += 1
                if stream1[len(stream1)-x] < stream2:
                    return True
                else:
                    return False

    # Check if stream1 has crossed over stream2
    else:
        if stream1[1-len(stream1)] <= stream2[1-len(stream2)]:
            return False
        else:
            if stream1[1-len(stream1)] > stream2[2-len(stream2)]:
                return False
            elif stream1[2-len(stream1)] < stream2[2-len(stream2)]:
                return True
            else:
                x = 2
                while stream1[len(stream1)-x] == stream2[len(stream2)-x]:
                    x += 1
                if stream1[len(stream1)-x] < stream2[len(stream2)-x]:
                    return True
                else:
                    return False

# Returns true if stream1 crossed under stream2 in most recent candle, stream2 can be integer/float or data array
def CrossesUnder(stream1, stream2):
    # If stream2 is an int or float, check if stream1 has crossed under that fixed number
    if isinstance(stream2, int) or isinstance(stream2, float):
        if stream1[len(stream1)-1] >= stream2:
            return False
        else:
            if stream1[len(stream1)-2] < stream2:
                return False
            elif stream1[len(stream1)-2] > stream2:
                return True
            else:
                x = 2
                while stream1[len(stream1)-x] == stream2:
                    x += 1
                if stream1[len(stream1)-x] > stream2:
                    return True
                else:
                    return False
    # Check if stream1 has crossed under stream2
    else:
        if stream1[1-len(stream1)] >= stream2[len(stream2)]:
            return False
        else:
            if stream1[len(stream1)-2] < stream2[len(stream2)-2]:
                return False
            elif stream1[len(stream1)-2] > stream2[len(stream2)-2]:
                return True
            else:
                x = 2
                while stream1[len(stream1)-x] == stream2[len(stream2)-x]:
                    x = x + 1
                if stream1[len(stream1)-x] > stream2[len(stream2)-x]:
                    return True
                else:
                    return False



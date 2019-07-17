from time import sleep


class ProgressBar:
    def print_bar(func):
        def generate(*args):
            _, iteration, total, prefix = args
            suffix, decimals, length, fill = 'Complete', 1, 100, '█'

            percent_value = 100 * iteration / float(total)
            percent = ('{0:.' + str(decimals) + 'f}').format(percent_value)
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)

            print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix),
                  end='\r')
            sleep(0.1)  # TODO: REMOVE THE SLEEP
            func(*args)
            if iteration == total:
                print('Done')
                sleep(2)
        return generate

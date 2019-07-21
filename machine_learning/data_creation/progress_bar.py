from time import sleep


class ProgressBar:
    def print_bar(func):
        def generate(*args):
            _, iteration, total, prefix, _, _ = args
            suffix, decimals, length, fill = 'Complete', 1, 100, '█'

            percent_value = 100 * iteration / float(total)
            percent = ('{0:.' + str(decimals) + 'f}').format(percent_value)
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)

            print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix),
                  end='\r')

            func(*args)
            if iteration == total:
                print('Done')

        return generate

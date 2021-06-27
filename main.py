import utils
import parsing

if __name__ == "__main__":
    options = utils.args_parsing()
    utils.check_valid_options(options)
    parser = parsing.Parser(options)
    parser.main_parsing()
    parser.verify_parsing_content()

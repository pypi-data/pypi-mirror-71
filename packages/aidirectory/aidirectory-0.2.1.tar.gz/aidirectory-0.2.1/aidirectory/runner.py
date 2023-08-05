import os
import oyaml as yaml
import aidirectory.utils as utils
import aidirectory as ai


def run(
    project, topics, methods, isotherms, gradients, parameters, baseline, tg_methods,
):
    try:
        os.mkdir(project)
    except OSError:
        pass
    try:
        os.mkdir(parameters)
    except OSError:
        pass
    try:
        os.mkdir(baseline)
    except OSError:
        pass
    try:
        os.mkdir(tg_methods)
    except OSError:
        pass
    for topic in topics:
        topicpath = os.path.join(project, topic)
        try:
            os.mkdir(topicpath)
        except OSError:
            pass
        if isotherms:
            isograd = os.path.join(topicpath, "isotherm")
            try:
                os.mkdir(isograd)
            except OSError:
                pass
            utils.isograder(isograd, isotherms, methods)

        if gradients:
            isograd = os.path.join(topicpath, "gradient")
            try:
                os.mkdir(isograd)
            except OSError:
                pass
            utils.isograder(isograd, gradients, methods)


def main():
    def represent_none(self, _):
        return self.represent_scalar("tag:yaml.org,2002:null", "")

    yaml.add_representer(type(None), represent_none)

    parameters = os.path.join(os.getcwd(), "parameters.yaml")
    try:
        with open(parameters, "r") as stream:
            data_loaded = yaml.safe_load(stream)
    except FileNotFoundError as e:
        data_loaded = utils.write_yaml()
        with open("parameters.yaml", "w") as outfile:
            yaml.dump(data_loaded, outfile, default_flow_style=False)
        print("Please fill out the parameter.yaml document")
        try:
            os.startfile(os.path.join(os.getcwd(), "parameters.yaml"))
        except OSError:
            pass
    try:
        run(*utils.decompress(data_loaded))
    except TypeError as e:
        print("Please double-check your parameters.yaml document'")
        try:
            os.startfile(os.path.join(os.getcwd(), "parameters.yaml"))
        except OSError:
            pass
    new_data, write_path = utils.write_post_yaml(data_loaded)
    try:
        with open(write_path, "w") as outfile:
            yaml.dump(new_data, outfile, default_flow_style=False)
        with open(
            os.path.join(new_data.get("DIRECTORY"), "compile.CMD"), "w"
        ) as outfile:
            cmdlet = ai.cmd()
            outfile.writelines(cmdlet)
    except FileNotFoundError as e:
        pass


if __name__ == "__main__":
    main()

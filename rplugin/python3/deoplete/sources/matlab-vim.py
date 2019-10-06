import json

import matlab.engine

from deoplete.base.source import Base


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)
        self.name = "matlab"
        self.mark = "[matlab]"
        self.filetypes = ["matlab"]
        # vim.vars['ここにg:より右の変数名を書く']
        # 変数を取得して任意の長さまでにするとか
        self.rank = 500
        self.eng = matlab.engine.start_matlab()
        self.eng.eval("import com.mathworks.jmi.tabcompletion.*", nargout=0)
        self.eng.eval("tc=TabCompletionImpl();", nargout=0)

    def gather_candidates(self, context):
        i = context["input"]
        self.eng.eval(f'f=tc.getJSONCompletions("{i}",{len(i)});', nargout=0)
        coms_dict = json.loads(self.eng.eval("f.get()"))
        result = []
        try:
            for x in coms_dict["finalCompletions"]:
                word = x["popupCompletion"]
                # if self.eng.eval(f"exist {word} builtin;", nargout=1) == 5:
                #     word = word + "()"
                result.append({"word": word, "dup": 1})
        except KeyError:
            return None
        except matlab.engine.MatlabExecutionError:
            return None
        return result

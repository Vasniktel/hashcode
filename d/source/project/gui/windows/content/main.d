module project.gui.windows.content.main;

/// Main window content description

import project.gui.windows.instantiator.instantiator;
import dlangui;

const BasicWindowInstantiator instantiator;
enum windowId = "main";
enum parentId = null;

/// Window content described in DML language
private enum gui = q{
  VerticalLayout {
    backgroundColor: "#D3DAE3"
    margins: 10
    padding: 20
    TableLayout {
      colCount: 4
      TextWidget {
        fontSize: 15px
        text: "Choose file to load:"
      }
      HSpacer {}
      ImageButton {
        drawableId: "fileopen"
        id: openFileButton
        maxHeight: 40px
      }
      TextWidget {
        id: openFileNameWidget
        fontSize: 15px
        fontItalic: true
      }
      TextWidget {
        fontSize: 15px
        text: "Choose file to save result:"
      }
      HSpacer {}
      ImageButton {
        drawableId: "fileopen"
        id: saveFileButton
        maxHeight: 40px
      }
      TextWidget {
        id: saveFileNameWidget
        fontSize: 15px
        fontItalic: true
      }
    }
    VSpacer { minHeight: 5px }
    TextWidget {
      text: "Input data:"
      fontSize: 15px
      alignment: center
    }
    EditBox {
      id: inputEditBox
      fontSize: 15px
      minHeight: 500px
      minWidth: 700px
      showLineNumbers: true
    }
    VSpacer {}
    Button {
      id: proceedButton
      text: "Proceed"
      fontSize: 15px
    }
  }
};

/// Handlers assigned to specific widgets
private enum guiHandlers = [
  "proceedButton": ["project.gui.windows.handlers.main.ProceedButtonPressed"],
  "openFileButton": ["project.gui.windows.handlers.main.OpenFileButtonPressed"],
  "saveFileButton": ["project.gui.windows.handlers.main.SaveFileButtonPressed"]
];

/// Module constructor
static this() @system {
  const WindowInitParams params = {
    caption: UIString.fromRaw("Course work"d),
    content: gui,
    handlers: guiHandlers
  };

  instantiator = new const BasicWindowInstantiator(params);
}

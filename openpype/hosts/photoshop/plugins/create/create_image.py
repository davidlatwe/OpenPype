import openpype.api
from avalon.vendor import Qt
from avalon import photoshop


class CreateImage(openpype.api.Creator):
    """Image folder for publish."""

    name = "imageDefault"
    label = "Image"
    family = "image"
    defaults = ["Main"]

    def process(self):
        groups = []
        layers = []
        create_group = False

        stub = photoshop.stub()
        useSelection = False
        if (self.options or {}).get("useSelection"):
            useSelection = True
            multiple_instances = False
            selection = stub.get_selected_layers()
            self.log.info("selection {}".format(selection))
            if len(selection) > 1:
                # Ask user whether to create one image or image per selected
                # item.
                msg_box = Qt.QtWidgets.QMessageBox()
                msg_box.setIcon(Qt.QtWidgets.QMessageBox.Warning)
                msg_box.setText(
                    "Multiple layers selected."
                    "\nDo you want to make one image per layer?"
                )
                msg_box.setStandardButtons(
                    Qt.QtWidgets.QMessageBox.Yes |
                    Qt.QtWidgets.QMessageBox.No |
                    Qt.QtWidgets.QMessageBox.Cancel
                )
                ret = msg_box.exec_()
                if ret == Qt.QtWidgets.QMessageBox.Yes:
                    multiple_instances = True
                elif ret == Qt.QtWidgets.QMessageBox.Cancel:
                    return

                if multiple_instances:
                    for item in selection:
                        if item.group:
                            groups.append(item)
                        else:
                            layers.append(item)
                else:
                    group = stub.group_selected_layers(self.name)
                    groups.append(group)

            elif len(selection) == 1:
                # One selected item. Use group if its a LayerSet (group), else
                # create a new group.
                if selection[0].group:
                    groups.append(selection[0])
                else:
                    layers.append(selection[0])
            elif len(selection) == 0:
                # No selection creates an empty group.
                create_group = True
        else:
            stub.select_layers(stub.get_layers())
            group = stub.group_selected_layers(self.name)
            groups.append(group)

        if create_group:
            group = stub.create_group(self.name)
            groups.append(group)

        for layer in layers:
            stub.select_layers([layer])
            group = stub.group_selected_layers(layer.name)
            groups.append(group)

        for group in groups:
            long_names = []
            group.name = group.name.replace(stub.PUBLISH_ICON, ''). \
                replace(stub.LOADED_ICON, '')

            if useSelection:
                subset_name = self.data["subset"] + group.name
            else:
                # use value provided by user from Creator
                subset_name = self.data["subset"]

            if group.long_name:
                for directory in group.long_name[::-1]:
                    name = directory.replace(stub.PUBLISH_ICON, '').\
                                      replace(stub.LOADED_ICON, '')
                    long_names.append(name)

            self.data.update({"subset": subset_name})
            self.data.update({"uuid": str(group.id)})
            self.data.update({"long_name": "_".join(long_names)})
            stub.imprint(group, self.data)
            # reusing existing group, need to rename afterwards
            if not create_group:
                stub.rename_layer(group.id, stub.PUBLISH_ICON + group.name)

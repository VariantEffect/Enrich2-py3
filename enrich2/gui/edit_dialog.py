#  Copyright 2016 Alan F Rubin
#
#  This file is part of Enrich2.
#
#  Enrich2 is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Enrich2 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Enrich2.  If not, see <http://www.gnu.org/licenses/>.

import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.simpledialog
import tkinter.ttk
from collections import OrderedDict
from sys import maxsize
import logging

from .dialog import CustomDialog
from .dialog_elements import FileEntry, IntegerEntry, Checkbox
from .dialog_elements import StringEntry, SectionLabel, DEFAULT_COLUMNS
from ..libraries.barcode import BarcodeSeqLib
from ..libraries.barcodeid import BcidSeqLib
from ..libraries.barcodevariant import BcvSeqLib
from ..libraries.basic import BasicSeqLib
from ..libraries.idonly import IdOnlySeqLib
from ..libraries.seqlib import SeqLib
from ..libraries.variant import VariantSeqLib
from ..base.utils import log_message

from tkinter.ttk import *


def clear_nones(d):
    """
    Return a copy of dictionary *d* with keys with value ``None`` removed.
    """
    if not isinstance(d, dict):
        return d
    else:
        return dict((k, clear_nones(v)) for k, v in d.items() if v is not None)


# All valid suffixes for a FASTQ file that can be recognized by Enrich2
_FASTQ_SUFFIXES = [x + y for x in (".fq", ".fastq") for y in ("", ".bz2", ".gz")]


#: Dictionary defining the layout of the edit UI elements in columns
#: Keys are class names and values are lists of tuples, one tuple per column
#: The column tuples contain keys to the dialog element's ``frame_dict`` member
element_layouts = {
                    "BcvSeqLib": [('main', 'counts',),
                                  ('fastq', 'trimming', 'filters',),
                                  ('barcodes', 'variants',)],
                    "BcidSeqLib":  [('main', 'counts',),
                                    ('fastq', 'trimming', 'filters',),
                                    ('barcodes', 'identifiers',)],
                    "BasicSeqLib": [('main', 'counts',),
                                    ('fastq', 'trimming', 'filters',),
                                    ('variants',)],
                    "BarcodeSeqLib": [('main', 'counts',),
                                      ('fastq', 'trimming', 'filters',),
                                      ('barcodes',)],
                    "IdOnlySeqLib":  [('main', 'counts',),
                                      ('identifiers',)],
                    "Selection": [('main',)],
                    "Condition": [('main',)],
                    "Experiment": [('main',)]
                   }


class CountsToggle(object):
    def __init__(self, frame_dict):
        self.mode = tk.StringVar()
        self.frame_dict = frame_dict
        self.rb_fastq = None
        self.rb_coutns = None

    def body(self, master, row, columns=DEFAULT_COLUMNS, **kwargs):
        self.rb_fastq = Radiobutton(
            master, text="FASTQ File Mode",
            variable=self.mode, value="FASTQ",
            command=self.fastq_mode
        )
        self.rb_fastq.grid(row=row, column=0, columnspan=columns, sticky="ew")
        self.rb_counts = Radiobutton(
            master, text="Count File Mode",
            variable=self.mode, value="Counts",
            command=self.counts_mode
        )
        self.rb_counts.grid(
            row=row + 1, column=0, columnspan=columns, sticky="ew")
        return 2

    def counts_mode(self):
        for k in ['filters', 'fastq', 'overlap', 'trimming']:
            if k in self.frame_dict:
                for x in self.frame_dict[k]:
                    try:
                        x.disable()
                    except AttributeError:
                        print(x, k)
        for k in ['counts']:
            if k in self.frame_dict:
                for x in self.frame_dict[k]:
                    try:
                        x.enable()
                    except AttributeError:
                        print(x, k)

    def fastq_mode(self):
        for k in ['counts']:
            if k in self.frame_dict:
                for x in self.frame_dict[k]:
                    try:
                        x.disable()
                    except AttributeError:
                        print(x, k)
        for k in ['filters', 'fastq', 'overlap', 'trimming']:
            if k in self.frame_dict:
                for x in self.frame_dict[k]:
                    try:
                        x.enable()
                    except AttributeError:
                        print(x, k)

    def validate(self):
        return True

    def apply(self):
        return None

    def enable(self):
        pass

    def disable(self):
        pass


class EditDialog(CustomDialog):
    """
    Dialog box for editing elements. Also used to set properties 
    on newly-created elements.

    *parent_window* is the Tk window that owns this child window
    *tree* is the object containing the config tree and associated Treeview
    *new* is ``True`` if we are creating a new child of the focused item or 
    ``False`` if we are editing the focused item
    """
    def __init__(self, parent_window, tree, element, title="Configure Object"):
        self.tree = tree
        self.element = element
        self.element_cfg = None
        self.frame_dict = OrderedDict()
        self.toggle = None
        self.parent_window = parent_window

        # create the editable version of the config object
        self.element_cfg = self.element.serialize()

        # dialog options common to all elements
        self.frame_dict['main'] = list()
        self.name_entry = StringEntry(
            "Name", self.element_cfg, 'name', optional=False
        )
        self.frame_dict['main'].append(self.name_entry)
        if 'output directory' in self.element_cfg:
            self.frame_dict['main'].append(
                FileEntry(
                    "Output Directory", self.element_cfg, 'output directory',
                    optional=self.element != self.tree.root_element,
                    directory=True
                )
            )
        if isinstance(self.element, SeqLib):
            self.frame_dict['counts'] = list()

            self.frame_dict['main'].append(SectionLabel("SeqLib Options"))
            self.frame_dict['main'].append(
                IntegerEntry("Time Point", self.element_cfg, 'timepoint'))

            self.frame_dict['counts'].append(SectionLabel("Counts Options"))
            self.frame_dict['counts'].append(
                FileEntry(
                    "Counts File", self.element_cfg,
                    'counts file', extensions=[".h5", ".txt", ".tsv", ".csv"]
                )
            )

            if not isinstance(self.element, IdOnlySeqLib):
                self.toggle = CountsToggle(self.frame_dict)
                self.frame_dict['main'].append(self.toggle)

                self.frame_dict['fastq'] = list()
                self.frame_dict['filters'] = list()

                self.frame_dict['filters'].append(
                    SectionLabel("FASTQ Filtering"))
                self.frame_dict['filters'].append(
                    IntegerEntry(
                        "Minimum Quality",
                        self.element_cfg['fastq']['filters'],
                        'min quality', optional=True)
                )
                self.frame_dict['filters'].append(
                    IntegerEntry(
                        "Average Quality",
                        self.element_cfg['fastq']['filters'],
                        'avg quality', optional=True)
                )
                self.frame_dict['filters'].append(
                    IntegerEntry(
                        "Maximum N's", self.element_cfg['fastq']['filters'],
                        'max N', optional=True)
                )
                self.frame_dict['fastq'].append(SectionLabel("FASTQ Options"))

            elif 'fastq' in self.frame_dict:
                self.frame_dict['fastq'].append(
                    FileEntry(
                        "Reads", self.element_cfg['fastq'],
                        'reads', extensions=_FASTQ_SUFFIXES
                    )
                )
                self.frame_dict['fastq'].append(
                    Checkbox("Reverse", self.element_cfg['fastq'], 'reverse'))

            if isinstance(self.element, BarcodeSeqLib) or \
                    isinstance(self.element, BasicSeqLib):
                self.frame_dict['trimming'] = list()
                self.frame_dict['trimming'].append(
                    SectionLabel("Read Trimming Options"))
                self.frame_dict['trimming'].append(
                    IntegerEntry(
                        "Trim Start", self.element_cfg['fastq'],
                        'start', optional=True, minvalue=1
                    )
                )
                self.frame_dict['trimming'].append(
                    IntegerEntry(
                        "Trim Length", self.element_cfg['fastq'],
                        'length', optional=True, minvalue=1
                    )
                )

            if isinstance(self.element, BarcodeSeqLib):
                self.frame_dict['barcodes'] = list()
                self.frame_dict['barcodes'].append(
                    SectionLabel("Barcode Options"))
                if isinstance(self.element, BcvSeqLib) or \
                        isinstance(self.element, BcidSeqLib):
                    self.frame_dict['barcodes'].append(
                        FileEntry(
                            "Barcode-variant File",
                            self.element_cfg['barcodes'], 'map file'
                        )
                    )
                self.frame_dict['barcodes'].append(
                    IntegerEntry(
                        "Minimum Count", self.element_cfg['barcodes'],
                        'min count', optional=True
                    )
                )

            if isinstance(self.element, BcidSeqLib) or \
                    isinstance(self.element, IdOnlySeqLib):
                self.frame_dict['identifiers'] = list()
                self.frame_dict['identifiers'].append(
                    SectionLabel("Identifier Options"))
                self.frame_dict['identifiers'].append(
                    IntegerEntry(
                        "Minimum Count", self.element_cfg['identifiers'],
                        'min count', optional=True
                    )
                )

            if isinstance(self.element, VariantSeqLib):
                self.frame_dict['variants'] = list()
                self.frame_dict['variants'].append(
                    SectionLabel("Variant Options"))
                self.frame_dict['variants'].append(
                    StringEntry(
                        "Wild Type Sequence",
                        self.element_cfg['variants']['wild type'], 'sequence'
                    )
                )
                self.frame_dict['variants'].append(
                    IntegerEntry(
                        "Wild Type Offset",
                        self.element_cfg['variants']['wild type'],
                        'reference offset', optional=True, minvalue=-maxsize
                    )
                )
                self.frame_dict['variants'].append(
                    Checkbox(
                        "Protein Coding",
                        self.element_cfg['variants']['wild type'], 'coding')
                )
                self.frame_dict['variants'].append(
                    IntegerEntry(
                        "Minimum Count", self.element_cfg['variants'],
                        'min count', optional=True
                    )
                )
                self.frame_dict['variants'].append(
                    IntegerEntry(
                        "Maximum Mutations", self.element_cfg['variants'],
                        'max mutations', optional=True
                    )
                )
                self.frame_dict['variants'].append(
                    Checkbox(
                        "Use Aligner",
                        self.element_cfg['variants'], 'use aligner'
                    )
                )
        CustomDialog.__init__(self, parent_window, title)

    def body(self, master):
        """
        Add the UI elements to the edit window. Ordering and placement of UI 
        elements in columns is defined by the ``element_layouts`` dictionary.
        """
        main = Frame(master, padding=(3, 3, 12, 12))
        main.grid(row=0, column=0, sticky="nsew")

        layout = element_layouts[type(self.element).__name__]
        for i, column_tuple in enumerate(layout):
            new_frame = Frame(master, padding=(3, 3, 12, 12))
            new_frame.grid(row=0, column=i, sticky="nsew")
            row_no = 0
            for row_frame_key in layout[i]:
                for ui_element in self.frame_dict[row_frame_key]:
                    row_no += ui_element.body(new_frame, row_no, left=True)
        if 'fastq' in self.frame_dict:
            if self.element.counts_file is not None:
                self.toggle.rb_counts.invoke()
            else:
                self.toggle.rb_fastq.invoke()

    def validate(self):
        """
        Called when the user chooses "OK", before closing the box.

        Also checks that child name is unique.
        """
        for tk_list in self.frame_dict.values():
            if not all(x.validate() for x in tk_list):
                return False

        if self.element.parent is not None:
            if self.element not in self.element.parent.children:
                if self.name_entry.value.get() in \
                        self.element.parent.child_names():
                    tkinter.messagebox.showwarning(
                        "", "Sibling names must be unique.")
                    return False
        return True

    def apply(self):
        """
        Called when the user chooses "OK" and the box closes.
        """
        # apply all changes to the config object
        for tk_list in self.frame_dict.values():
            for tk_element in tk_list:
                tk_element.apply()

        current_cfg = self.element.serialize()
        try:
            if isinstance(self.element, SeqLib):
                self.element.configure(clear_nones(self.element_cfg))
            else:
                self.element.configure(
                    clear_nones(self.element_cfg),
                    configure_children=False, init_from_gui=True)

            # insert into the object if necessary
            if self.element.parent is not None:
                if self.element:
                    self.element.parent.add_child(self.element)
                    self.parent_window.refresh_treeview()

        except Exception as e:
            # Reset the attempted edit
            if isinstance(self.element, SeqLib):
                self.element.configure(clear_nones(current_cfg))
            else:
                self.element.configure(
                    clear_nones(current_cfg),
                    configure_children=False, init_from_gui=True)
            log_message(
                logging.exception, e, extra={"oname": self.element.name}
            )
            tkinter.messagebox.showwarning(
                title="Configuration Error!",
                message="The following error was encountered when trying to "
                        "configure element with name '{}':\n\n{}\n\nSee log "
                        "for details".format(self.element.name, e)
            )

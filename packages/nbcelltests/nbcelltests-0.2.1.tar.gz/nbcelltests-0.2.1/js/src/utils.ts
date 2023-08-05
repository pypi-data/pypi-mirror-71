/******************************************************************************
 *
 * Copyright (c) 2019, the nbcelltest authors.
 *
 * This file is part of the nbcelltest library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */
import {JupyterFrontEnd} from "@jupyterlab/application";
import {IDocumentManager} from "@jupyterlab/docmanager";

export
const CELLTESTS_CATEGORY = "Celltests";

export
const CELLTESTS_TEST_ID = "celltests:test";

export
const CELLTESTS_LINT_ID = "celltests:lint";

export
const CELLTESTS_TEST_CAPTION = "Run Celltests";

export
const CELLTESTS_LINT_CAPTION = "Run Lint";

export
const CELLTEST_TOOL_CLASS = "CelltestTool";

export
const CELLTEST_TOOL_CONTROLS_CLASS = "CelltestsControls";

export
const CELLTEST_TOOL_RULES_CLASS = "CelltestsRules";

export
const CELLTEST_TOOL_EDITOR_CLASS = "CelltestsEditor";

export
function isEnabled(app: JupyterFrontEnd, docManager: IDocumentManager): () => boolean {
  return () => (app.shell.currentWidget &&
                docManager.contextForWidget(app.shell.currentWidget) &&
                docManager.contextForWidget(app.shell.currentWidget).model) ? true : false;
}

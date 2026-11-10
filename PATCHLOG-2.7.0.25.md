# Virtue Assistant 2.7.0.25

Built from 2.7.0.24. The files you install are now about a third smaller to download. Every feature, window,
setting and saved file is the same as in 2.7.0.24. If anything misbehaves, go back to 2.7.0.24.

## Shard rules (In Mani Ylem)

- No game action was added or changed. The same presses do the same single things, so R1-R8 are untouched.

## Changed

- **All files:** the main script and every module are packed tighter: tabs for indents, fewer spaces, shorter
  names for values used only inside one function, and a few shared helpers named once at the top of each
  module. Together the files are 63% of their old size. What the code does is unchanged, and your saved
  settings, positions and files load as before.
- **Readable copy:** the same code, laid out normally and with comments, is in the `readable` folder of the
  GitHub page, for anyone who wants to read how it works. You don't need it to play.
- **Main script:** What's new lists this version.

## The review pass

- Rules check R1-R8: no new game action calls.
- The packed files were checked against the normal ones, function by function: the same program, with only
  the layout and the inner names changed. The lines TazUO reads itself (the `import API` lines, the values the
  Script Constants editor shows, each module's registration line) are the same.
- Also run, on both the normal and the packed files:
  - the IronPython 3.4 compile;
  - the mock run, with and without every module, giving the same results;
  - each module run on its own;
  - the call counter, showing no rise in calls or client hops per pass.
- All item tests pass on the normal files.

## Install

Copy `VirtueAssistantV2-7-0-25.py` and the `VirtueAssistantModules` folder into `TazUO/LegionScripts/`, as
before: the files at the top of the GitHub page, or the zip from the Releases page, which unzips straight into
`TazUO/LegionScripts/`. Replace the whole modules folder, then run the main script. You can delete the 2.7.0.24
main script. The `readable` folder on the GitHub page is the same code with comments; don't install it.

Only in game:
- That the main script starts and every module, part and Settings page works as in 2.7.0.24.
- That a module run on its own from the Script Manager starts as before.
- That Edit Constants on the main script shows and saves its values as before.
- That error lines in the journal, if any, still name a file and line (they now point at the packed files).

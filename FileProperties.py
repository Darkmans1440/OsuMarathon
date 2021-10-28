import os.path


class TimeableObject:

    def __init__(self, rawdata: [str], start_index: int, end_index: int):
        self._rawdata = rawdata.split(",")
        self._start_index = start_index
        self._end_index = end_index

    def increment_start_end_times(self, new_time: int):
        pass

    def get_start_index(self):
        return self._start_index

    def get_end_index(self):
        return self._end_index

    def get_start_time(self):
        return int(float(self._rawdata[self._start_index]))

    def get_end_time(self):
        return int(float(self._rawdata[self._end_index]))

    def get_rawdata(self):
        return self._rawdata

    def __str__(self):
        return ",".join(self._rawdata)


class TimingPoint(TimeableObject):

    def __init__(self, rawdata: str):
        super().__init__(rawdata, 0, 0)

    def increment_start_end_times(self, new_time: int):
        self.get_rawdata()[self.get_start_index()] = str(max(0, self.get_start_time() + new_time))

    def get_end_time(self):
        return -1

    def normalize_to(self, average_bpm: float):
        self.get_rawdata()[1] = str(-100 / (average_bpm / self.get_bpm()))

    def get_bpm(self):
        return 1 / float(self.get_rawdata()[1]) * 1000 * 60

    def set_inherited(self, value: bool):
        self.get_rawdata()[6] = str(0 if value else 1)

    def is_inherited(self):
        return False if "1" in self.get_rawdata()[6] else True


class HitObject(TimeableObject):

    def __init__(self, rawdata: str):
        super().__init__(rawdata, 2, 0)

    def get_end_time(self):
        value = int(
            float(self.get_rawdata()[5].split(":")[self.get_end_index()]) if len(self.get_rawdata()) >= 6 else -1)
        return -1 if value == 0 else value

    def increment_start_end_times(self, new_time: int):
        self.get_rawdata()[self.get_start_index()] = str(int(self.get_start_time() + new_time))
        end_time = self.get_end_time()

        if end_time != -1:
            end_time_length = len(str(end_time))
            content_beyond_end_time = self.get_rawdata()[5][end_time_length:]
            self.get_rawdata()[5] = str(end_time + new_time) + content_beyond_end_time


class OsuProperties:

    def __init__(self, filename):
        self._lines = []
        self._timingpoints = []
        self._hitobjects = []
        self._filename = filename
        self._properties = {}
        self._background = ""

    def mutate_append_timingpoint(self, spacing: int, timingpoint: 'TimingPoint'):
        timingpoint.increment_start_end_times(spacing)
        self._timingpoints.append(timingpoint)
        return timingpoint

    def mutate_append_hitobject(self, spacing: int, hitobject: 'HitObject'):
        hitobject.increment_start_end_times(spacing)
        self._hitobjects.append(hitobject)
        return hitobject

    def append(self, osu_properties: 'OsuProperties', spacing: int):

        length = spacing

        for timingpoint in osu_properties._timingpoints:
            new_object = TimingPoint(timingpoint.get_rawdata())
            new_object.increment_start_end_times(length)

            self._timingpoints.append(new_object)

        for hitobject in osu_properties._hitobjects:
            new_object = HitObject(hitobject.get_rawdata())
            new_object.increment_start_end_times(length)

            self._hitobjects.append(new_object)

    def get_average_bpm_osu_style(self):

        average_bpm = self.get_average_bpm()

        num = int(average_bpm)

        if average_bpm - num <= 0.5:
            return num
        else:
            return num + 1

    def get_average_bpm(self):

        timingpoints_sorted = sorted(self._timingpoints, key=lambda x: x.get_start_time())
        timingpoints_sorted = list(filter(lambda value: not value.is_inherited(), timingpoints_sorted))

        size = len(timingpoints_sorted)
        values = {}

        average_bpm = 0
        longest_bpm_time = 0

        for i in range(size):

            current_timingpoint = timingpoints_sorted[i]

            if i + 1 >= size:
                end_time = self.get_length()
            else:
                end_time = timingpoints_sorted[i + 1].get_start_time()

            bpm = timingpoints_sorted[i].get_bpm()
            end_time -= current_timingpoint.get_start_time()
            current = values.get(bpm)

            if current is None:
                current = 0

            current += end_time
            values[bpm] = current

            if current > longest_bpm_time:
                average_bpm = bpm
                longest_bpm_time = current

        return average_bpm

    def get_first_note_time(self):

        if len(self._hitobjects) == 0:
            return -1

        hitobjects_sorted = sorted(self._hitobjects, key=lambda x: x.get_start_time())

        return hitobjects_sorted[0].get_start_time()

    def get_length(self):

        highest = 0

        for hitobject in self._hitobjects:

            to_check = hitobject.get_start_time() if hitobject.get_end_time() < hitobject.get_start_time() else hitobject.get_end_time()

            if to_check > highest:
                highest = to_check

        return highest

    def get_filename(self):
        return self._filename

    def get_background(self):
        return self._background

    def set_background(self, new_value: str):
        self._background = new_value

    def get_timingpoints(self) -> list[TimingPoint]:
        return self._timingpoints

    def get_hitobjects(self) -> list[HitObject]:
        return self._hitobjects

    def exists_and_read(self):

        if not os.path.isfile(self._filename):
            return False

        self._read()
        return True

    def get_properties(self, field: str):
        return self._properties.get(field)

    def set_property(self, field: str, key: str, value: str):

        properties = self._properties.get(field)

        if properties is None:
            properties = {}
            self._properties[field] = properties

        properties[key] = value

    def write(self, new_location: str):

        with open(new_location, mode='w', encoding="utf-8") as file:
            file.write("osu file format v14\n")

            for properties_name, properties in self._properties.items():
                file.write("\n" + properties_name + "\n")

                for property_name, property_value in properties.items():

                    if "[Metadata]" in properties_name or "[Difficulty]" in properties_name:
                        file.write(property_name + ":" + property_value + "\n")
                    else:
                        file.write(property_name + ": " + property_value + "\n")

            file.write("\n[Events]\n")
            file.write("//Background and Video events\n")
            if self._background is not None:
                file.write("0,0,\"{}\",0,0".format(self._background) + "\n")
            file.write("//Break Periods\n")
            file.write("//Storyboard Layer 0 (Background)\n")
            file.write("//Storyboard Layer 1 (Fail)\n")
            file.write("//Storyboard Layer 2 (Pass)\n")
            file.write("//Storyboard Layer 3 (Foreground)\n")
            file.write("//Storyboard Layer 4 (Overlay)\n")
            file.write("//Storyboard Sound Samples\n")

            file.write("\n[TimingPoints]\n")
            for timingpoint in self._timingpoints:
                file.write(str(timingpoint) + "\n")

            file.write("\n[HitObjects]\n")
            for hitobject in self._hitobjects:
                file.write(str(hitobject) + "\n")

    def _read(self):

        self._properties.clear()

        current_type = None

        with open(self._filename, 'r', encoding="utf-8") as file:

            for line in file.readlines():

                line = line.strip()

                if len(line) == 0:
                    continue

                self._lines.append(line)

                if line.startswith("["):
                    current_type = line
                    continue

                if current_type == "[Events]":
                    if "," in line:
                        self._background = line.split(",")[2].strip('"')
                if current_type == "[HitObjects]":
                    self._hitobjects.append(HitObject(line))
                    continue
                if current_type == "[TimingPoints]":
                    self._timingpoints.append(TimingPoint(line))
                    continue

                splitline = line.split(':')

                if len(splitline) < 2:
                    continue

                self.set_property(current_type, splitline[0], splitline[1].strip())
